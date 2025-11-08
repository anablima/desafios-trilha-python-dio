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
        # Insere placeholder automaticamente após primeira ocorrência da imagem da badge de coverage, se existir.
        if BADGE_IMG_RE.search(content):
            def _insert_placeholder(m: re.Match) -> str:
                return f"{m.group(0)} Cobertura: <!--COVERAGE_PCT-->{pct_display}<!--/COVERAGE_PCT-->"
            content_with_placeholder = BADGE_IMG_RE.sub(_insert_placeholder, content, count=1)
            content = content_with_placeholder
            print('Placeholder de cobertura inserido automaticamente.')
        else:
            print('Badge de coverage não encontrada; placeholder não inserido.')
            return False
        # Reexecuta regex após inserção
        match = PLACEHOLDER_RE.search(content)

    if match is None:  # salvaguarda estática (já tratado, mas satisfaz analisador)
        print('Falha ao localizar placeholder após tentativa de inserção.')
        return False
    atual = match.group(2).strip()
    if atual == pct_display:
        new_content = content  # Mesmo valor, apenas garantimos cache-bust
    else:
        new_content = PLACEHOLDER_RE.sub(rf"\g<1>{pct_display}\g<3>", content, count=1)

    # Atualiza link da imagem adicionando query param cache-bust ?v=<pct>
    def _badge_sub(m: re.Match) -> str:
        base = m.group(1)
        pct_query = pct_display.rstrip('%')
        return f"{base}?v={pct_query})"

    if BADGE_IMG_RE.search(new_content):
        new_content = BADGE_IMG_RE.sub(_badge_sub, new_content, count=1)

    changed = new_content != README.read_text(encoding='utf-8')
    if changed:
        README.write_text(new_content, encoding='utf-8')
        print(f'Readme atualizado / sincronizado com cobertura {pct_display}')
    else:
        print('Nenhuma alteração necessária no README.')
    return changed


def main() -> int:
    update_readme()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
