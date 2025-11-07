<<<<<<< HEAD
"""Gera badge de cobertura (apenas linhas) a partir do arquivo `.coverage`.
Não depende mais de coverage.xml.
Thresholds:
  >=90 brightgreen, >=80 green, >=70 yellowgreen, >=60 yellow, >=50 orange, <50 red.
=======
"""Gera badge de cobertura.
Prioridade:
1. Usa coverage.xml (line-rate e branch-rate) se existir.
     - Se branch-rate disponível, mostra "branches".
     - Caso contrário, usa line-rate.
2. Fallback heurístico em .coverage (executed/missing) se xml ausente.

Thresholds (branch ou linha):
    >=85 brightgreen
    >=75 green
    >=65 yellowgreen
    >=55 yellow
    >=45 orange
    <45 red
>>>>>>> 87fe096 (ci: adiciona workflow de testes com cobertura de ramos e atualiza badge)
"""
from __future__ import annotations
from pathlib import Path
import re
import xml.etree.ElementTree as ET

BADGE_FILE = Path("coverage-badge.svg")
COVERAGE_DATA = Path(".coverage")
<<<<<<< HEAD

def pct_to_color(pct: float) -> str:
    if pct >= 90: return "brightgreen"
    if pct >= 80: return "green"
    if pct >= 70: return "yellowgreen"
    if pct >= 60: return "yellow"
    if pct >= 50: return "orange"
    return "red"

def parse_coverage() -> float:
=======
XML_PATH = Path("coverage.xml")


def pct_to_color(pct: float) -> str:
    if pct >= 85: return "brightgreen"
    if pct >= 75: return "green"
    if pct >= 65: return "yellowgreen"
    if pct >= 55: return "yellow"
    if pct >= 45: return "orange"
    return "red"


def parse_coverage() -> tuple[float, str]:
    """Retorna (percentual, tipo) onde tipo é 'branches' ou 'lines'."""
    if XML_PATH.exists():
        try:
            root = ET.parse(XML_PATH).getroot()
            branch_rate = root.attrib.get('branch-rate')
            line_rate = root.attrib.get('line-rate')
            if branch_rate is not None:
                return float(branch_rate) * 100.0, 'branches'
            if line_rate is not None:
                return float(line_rate) * 100.0, 'lines'
        except Exception:
            pass
    # Fallback heurístico em .coverage (executed/missing)
>>>>>>> 87fe096 (ci: adiciona workflow de testes com cobertura de ramos e atualiza badge)
    try:
        text = COVERAGE_DATA.read_text(errors='ignore')
        executed_match = re.search(r'"executed"\s*:\s*(\d+)', text)
        missing_match = re.search(r'"missing"\s*:\s*(\d+)', text)
        if executed_match and missing_match:
            executed = int(executed_match.group(1))
            missing = int(missing_match.group(1))
            total = executed + missing
            if total:
<<<<<<< HEAD
                return executed / total * 100.0
    except FileNotFoundError:
        pass
    return 0.0

def build_svg(pct: float) -> str:
    pct_str = f"{pct:.0f}%"
    color = pct_to_color(pct)
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='125' height='20'>
=======
                return executed / total * 100.0, 'lines'
    except FileNotFoundError:
        pass
    return 0.0, 'lines'


def build_svg(pct: float, kind: str) -> str:
        pct_str = f"{pct:.0f}%"
        color = pct_to_color(pct)
        label = 'coverage'
        if kind == 'branches':
                label = 'branches'
        return f"""<svg xmlns='http://www.w3.org/2000/svg' width='140' height='20'>
>>>>>>> 87fe096 (ci: adiciona workflow de testes com cobertura de ramos e atualiza badge)
<linearGradient id='b' x2='0' y2='100%'><stop offset='0' stop-color='#bbb' stop-opacity='.1'/><stop offset='1' stop-opacity='.1'/></linearGradient>
<mask id='a'><rect width='140' height='20' rx='3' fill='#fff'/></mask>
<g mask='url(#a)'>
<<<<<<< HEAD
  <rect width='65' height='20' fill='#555'/>
  <rect x='65' width='60' height='20' fill='#{'4c1' if color=='brightgreen' else '2ea44f' if color=='green' else 'a4a61d' if color=='yellowgreen' else 'e3b341' if color=='yellow' else 'fe7d37' if color=='orange' else 'e05d44'}'/>
  <rect width='125' height='20' fill='url(#b)'/>
</g>
=======
    <rect width='80' height='20' fill='#555'/>
    <rect x='80' width='60' height='20' fill='#{'4c1' if color=='brightgreen' else '2ea44f' if color=='green' else 'a4a61d' if color=='yellowgreen' else 'e3b341' if color=='yellow' else 'fe7d37' if color=='orange' else 'e05d44'}'/>
    <rect width='140' height='20' fill='url(#b)'/>
  </g>
>>>>>>> 87fe096 (ci: adiciona workflow de testes com cobertura de ramos e atualiza badge)
<g fill='#fff' text-anchor='middle' font-family='Verdana,Geneva,DejaVu Sans,sans-serif' font-size='11'>
    <text x='40' y='15' fill='#010101' fill-opacity='.3'>{label}</text>
    <text x='40' y='15'>{label}</text>
    <text x='110' y='15' fill='#010101' fill-opacity='.3'>{pct_str}</text>
    <text x='110' y='15'>{pct_str}</text>
</g>
</svg>"""

def main() -> int:
<<<<<<< HEAD
    pct = parse_coverage()
    new_svg = build_svg(pct)
    old_svg = BADGE_FILE.read_text() if BADGE_FILE.exists() else ""
    if old_svg != new_svg:
        BADGE_FILE.write_text(new_svg)
        print(f"Badge atualizado para {pct:.2f}% (linhas)")
=======
    pct, kind = parse_coverage()
    new_svg = build_svg(pct, kind)
    old_svg = BADGE_FILE.read_text() if BADGE_FILE.exists() else ""
    if old_svg != new_svg:
        BADGE_FILE.write_text(new_svg)
        print(f"Badge atualizado ({kind}) para {pct:.2f}%")
>>>>>>> 87fe096 (ci: adiciona workflow de testes com cobertura de ramos e atualiza badge)
    else:
        print("Badge já estava atualizado")
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
