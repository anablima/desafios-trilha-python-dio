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


def determine_pct() -> int:
    for fn in (read_pct_from_api, read_pct_from_badge):
        pct = fn()
        if pct is not None:
            return int(round(pct))
    return 0


def update_readme() -> bool:
    if not README.exists():
        print('README.md não encontrado')
        return False
    content = README.read_text(encoding='utf-8')
    pct = determine_pct()
    new_content, count = PLACEHOLDER_RE.subn(rf"\\1{pct}%\\3", content, count=1)
    if count == 0:
        print('Placeholder de cobertura não encontrado; nenhuma alteração.')
        return False
    if new_content != content:
        README.write_text(new_content, encoding='utf-8')
        print(f'Atualizado placeholder de cobertura para {pct}%')
        return True
    print('Valor de cobertura inalterado no README.')
    return False


def main() -> int:
    update_readme()
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
