"""Gera badge de cobertura (apenas linhas) a partir do arquivo `.coverage`.
Não depende de coverage.xml. Thresholds (linhas): >=90 brightgreen, >=80 green, >=70 yellowgreen, >=60 yellow, >=50 orange, <50 red.
"""
from __future__ import annotations
from pathlib import Path
import re
import os
import io

BADGE_FILE = Path("coverage-badge.svg")
COVERAGE_DATA = Path(".coverage")

def pct_to_color(pct: float) -> str:
    if pct >= 90: return "brightgreen"
    if pct >= 80: return "green"
    if pct >= 70: return "yellowgreen"
    if pct >= 60: return "yellow"
    if pct >= 50: return "orange"
    return "red"

def parse_coverage() -> float:
    """Obtém % de cobertura de linhas.

    1. Tenta carregar via API da biblioteca coverage (formato binário/SQLite padrão).
    2. Fallback para regex simples em caso de arquivo de teste textual (usado nos testes unitários).
    """
    # Primeiro: tentar via biblioteca coverage
    try:
        import coverage  # disponível via pytest-cov
        if COVERAGE_DATA.exists():
            cov = coverage.Coverage(data_file=str(COVERAGE_DATA))
            cov.load()
            # Usa buffer para descartar saída do relatório
            dummy = io.StringIO()
            pct = cov.report(file=dummy)  # retorna float
            return float(pct)
    except Exception:
        # Qualquer erro cai no fallback regex
        pass
    # Fallback textual (para testes que criam arquivo artificial)
    try:
        text = COVERAGE_DATA.read_text(errors='ignore')
        executed_match = re.search(r'"executed"\s*:\s*(\d+)', text)
        missing_match = re.search(r'"missing"\s*:\s*(\d+)', text)
        if executed_match and missing_match:
            executed = int(executed_match.group(1))
            missing = int(missing_match.group(1))
            total = executed + missing
            if total:
                return executed / total * 100.0
    except FileNotFoundError:
        pass
    return 0.0

def build_svg(pct: float) -> str:
    # Exibe uma casa decimal (ex.: 82.9%) para maior precisão percebida.
    pct_str = f"{pct:.1f}%"
    color = pct_to_color(pct)
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='125' height='20'>
<linearGradient id='b' x2='0' y2='100%'><stop offset='0' stop-color='#bbb' stop-opacity='.1'/><stop offset='1' stop-opacity='.1'/></linearGradient>
<mask id='a'><rect width='125' height='20' rx='3' fill='#fff'/></mask>
<g mask='url(#a)'>
  <rect width='65' height='20' fill='#555'/>
  <rect x='65' width='60' height='20' fill='#{'4c1' if color=='brightgreen' else '2ea44f' if color=='green' else 'a4a61d' if color=='yellowgreen' else 'e3b341' if color=='yellow' else 'fe7d37' if color=='orange' else 'e05d44'}'/>
  <rect width='125' height='20' fill='url(#b)'/>
</g>
<g fill='#fff' text-anchor='middle' font-family='Verdana,Geneva,DejaVu Sans,sans-serif' font-size='11'>
  <text x='33' y='15' fill='#010101' fill-opacity='.3'>coverage</text>
  <text x='33' y='15'>coverage</text>
  <text x='95' y='15' fill='#010101' fill-opacity='.3'>{pct_str}</text>
  <text x='95' y='15'>{pct_str}</text>
</g>
</svg>"""

def main() -> int:
    pct = parse_coverage()
    new_svg = build_svg(pct)
    old_svg = BADGE_FILE.read_text() if BADGE_FILE.exists() else ""
    if old_svg != new_svg:
        BADGE_FILE.write_text(new_svg)
        print(f"Badge atualizado para {pct:.2f}% (linhas)")
    else:
        print("Badge já estava atualizado")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
