"""Atualiza o placeholder de cobertura no README.

Procura por <!--COVERAGE_PCT-->X%<!--/COVERAGE_PCT--> e substitui X% pelo valor
inteiro arredondado da cobertura atual (derivado de coverage-badge.svg ou da API coverage).
"""
from __future__ import annotations
from pathlib import Path
import re
import io

README = Path('README.md')
BADGE = Path('coverage-badge.svg')
COVERAGE_FILE = Path('.coverage')

PLACEHOLDER_RE = re.compile(r'(<!--COVERAGE_PCT-->)([^<]*?)(<!--/COVERAGE_PCT-->)')
BADGE_IMG_RE = re.compile(r'(!\[Coverage\]\(coverage-badge\.svg)(?:\?v=[0-9.]+)?\)')


def read_pct_from_api() -> float | None:
    try:
        import coverage
        if COVERAGE_FILE.exists():
            cov = coverage.Coverage(data_file=str(COVERAGE_FILE))
            cov.load()
            dummy = io.StringIO()
            pct = cov.report(file=dummy)
            return float(pct)
    except Exception:
        return None
    return None


def read_pct_from_badge() -> float | None:
    if not BADGE.exists():
        return None
    text = BADGE.read_text(encoding='utf-8', errors='ignore')
    m = re.search(r">(\d+)%<", text)
    if m:
        try:
            return float(m.group(1))
        except ValueError:
            return None
    return None


def determine_pct() -> float:
    for fn in (read_pct_from_api, read_pct_from_badge):
        pct = fn()
        if pct is not None:
            return round(pct, 1)
    return 0.0


def update_readme() -> bool:
    if not README.exists():
        print('README.md não encontrado')
        return False
    content = README.read_text(encoding='utf-8')
    pct = determine_pct()
    pct_display = f"{pct:.1f}%"
    match = PLACEHOLDER_RE.search(content)
    if not match:
        print('Placeholder de cobertura não encontrado; nenhuma alteração.')
        return False
    atual = match.group(2).strip()
    if atual == pct_display:
        # Mesmo percentual; ainda assim garantir que badge tenha cache-bust correto
        new_content = content
    else:
        new_content = PLACEHOLDER_RE.sub(rf"\g<1>{pct_display}\g<3>", content, count=1)

    # Atualiza link da imagem adicionando query param cache-bust ?v=82.9 (sempre)
    # Atualiza imagem da badge se presente
    def _badge_sub(m: re.Match) -> str:
        base = m.group(1)
        pct_query = pct_display.rstrip('%')  # remove símbolo para query param
        return f"{base}?v={pct_query})"

    if BADGE_IMG_RE.search(new_content):
        new_content = BADGE_IMG_RE.sub(_badge_sub, new_content, count=1)
    else:
        # Se não houver imagem, opcionalmente podemos inserir após CI badge
        pass

    changed = new_content != content
    if changed:
        README.write_text(new_content, encoding='utf-8')
        print(f'Atualizado README cobertura para {pct_display}')
    else:
        print('Valor de cobertura inalterado no README (incluindo badge).')
    return changed


def main() -> int:
    update_readme()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
