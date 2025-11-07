"""Gera badge de cobertura baseado em coverage.xml.
Só atualiza arquivo se percentual mudar.
"""
from __future__ import annotations
import xml.etree.ElementTree as ET
from pathlib import Path

COVERAGE_XML = Path("coverage.xml")
BADGE_FILE = Path("coverage-badge.svg")

def pct_to_color(pct: float) -> str:
    if pct >= 90: return "brightgreen"
    if pct >= 80: return "green"
    if pct >= 70: return "yellowgreen"
    if pct >= 60: return "yellow"
    if pct >= 50: return "orange"
    return "red"

def build_svg(pct: float) -> str:
    pct_str = f"{pct:.0f}%"
    color = pct_to_color(pct)
    # Minimalistic SVG badge
    return f"""<svg xmlns='http://www.w3.org/2000/svg' width='120' height='20'>
<linearGradient id='b' x2='0' y2='100%'><stop offset='0' stop-color='#bbb' stop-opacity='.1'/><stop offset='1' stop-opacity='.1'/></linearGradient>
<mask id='a'><rect width='120' height='20' rx='3' fill='#fff'/></mask>
<g mask='url(#a)'>
  <rect width='60' height='20' fill='#555'/>
  <rect x='60' width='60' height='20' fill='#{'4c1' if color=='brightgreen' else '97CA00' if color=='green' else 'a4a61d' if color=='yellowgreen' else 'dfb317' if color=='yellow' else 'fe7d37' if color=='orange' else 'e05d44'}'/>
  <rect width='120' height='20' fill='url(#b)'/>
</g>
<g fill='#fff' text-anchor='middle' font-family='Verdana,Geneva,DejaVu Sans,sans-serif' font-size='11'>
  <text x='30' y='15' fill='#010101' fill-opacity='.3'>coverage</text>
  <text x='30' y='15'>coverage</text>
  <text x='90' y='15' fill='#010101' fill-opacity='.3'>{pct_str}</text>
  <text x='90' y='15'>{pct_str}</text>
</g>
</svg>"""

def main():
    if not COVERAGE_XML.exists():
        print("coverage.xml não encontrado")
        return 1
    tree = ET.parse(COVERAGE_XML)
    root = tree.getroot()
    rate = float(root.attrib.get("line-rate", 0.0)) * 100
    new_svg = build_svg(rate)
    old_svg = BADGE_FILE.read_text() if BADGE_FILE.exists() else ""
    if old_svg != new_svg:
        BADGE_FILE.write_text(new_svg)
        print(f"Badge atualizado para {rate:.2f}%")
    else:
        print("Badge já estava atualizado")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
