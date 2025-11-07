"""Gera badge de cobertura lendo arquivo .coverage (JSON interno do coverage >=5) ou fallback textual.
Atualiza somente se percentual mudar. Novos thresholds: 95/85/75/65/55.
"""
from __future__ import annotations
from pathlib import Path
import json
import re

BADGE_FILE = Path("coverage-badge.svg")
COVERAGE_DATA = Path(".coverage")  # arquivo binário/JSON criado pelo coverage.py


def pct_to_color(pct: float) -> str:
    if pct >= 95: return "brightgreen"
    if pct >= 85: return "green"
    if pct >= 75: return "yellowgreen"
    if pct >= 65: return "yellow"
    if pct >= 55: return "orange"
    return "red"


def parse_coverage_percentage() -> float:
    """Tenta ler percentual total de linhas da estrutura JSON interna.
    Fallback: extrai número de coverage.xml se existir (para compatibilidade transitória) ou retorna 0.
    """
    # coverage >=5 salva dados em formato de pickled/JSON dependendo da versão; para simplificar tentamos JSON
    try:
        text = COVERAGE_DATA.read_text(errors="ignore")
        # Heurística: procurar por chave 'lines' e 'executed' para calcular percentual.
        if '"lines"' in text and '"executed"' in text:
            # Busca padrões: "executed": <num>, "missing": <num>
            executed_match = re.search(r'"executed"\s*:\s*(\d+)', text)
            missing_match = re.search(r'"missing"\s*:\s*(\d+)', text)
            if executed_match and missing_match:
                executed = int(executed_match.group(1))
                missing = int(missing_match.group(1))
                total = executed + missing
                if total > 0:
                    return executed / total * 100.0
        # Tentativa de parse como JSON puro
        try:
            data = json.loads(text)
            # Estrutura não oficial, tentativa defensiva
            totals = data.get('totals') or {}
            if 'lines' in totals and isinstance(totals['lines'], dict):
                covered = totals['lines'].get('covered', 0)
                total = totals['lines'].get('total', 0)
                if total:
                    return covered / total * 100.0
        except Exception:
            pass
    except FileNotFoundError:
        pass

    # Fallback: se coverage.xml existir ainda, usar
    xml_path = Path('coverage.xml')
    if xml_path.exists():
        import xml.etree.ElementTree as ET
        try:
            root = ET.parse(xml_path).getroot()
            return float(root.attrib.get('line-rate', 0.0)) * 100.0
        except Exception:
            return 0.0
    return 0.0


def build_svg(pct: float) -> str:
    pct_str = f"{pct:.0f}%"
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
    pct = parse_coverage_percentage()
    new_svg = build_svg(pct)
    old_svg = BADGE_FILE.read_text() if BADGE_FILE.exists() else ""
    if old_svg != new_svg:
        BADGE_FILE.write_text(new_svg)
        print(f"Badge atualizado para {pct:.2f}%")
    else:
        print("Badge já estava atualizado")
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
