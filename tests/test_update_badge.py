import builtins
from pathlib import Path
import re
import importlib
import types

import pytest

# Importa o módulo de badge
badge_module = importlib.import_module('scripts.update_badge')


def write_coverage(tmp_path: Path, executed: int, missing: int):
    # Constrói conteúdo mínimo contendo os padrões "executed" e "missing" que o regex do script procura.
    data = f'"executed": {executed}, "missing": {missing}'
    cov_file = tmp_path / '.coverage'
    cov_file.write_text(data, encoding='utf-8')
    return cov_file


def test_pct_to_color_thresholds():
    pct_to_color = badge_module.pct_to_color
    assert pct_to_color(90) == 'brightgreen'
    assert pct_to_color(89.9) == 'green'
    assert pct_to_color(80) == 'green'
    assert pct_to_color(79.9) == 'yellowgreen'
    assert pct_to_color(70) == 'yellowgreen'
    assert pct_to_color(69.9) == 'yellow'
    assert pct_to_color(60) == 'yellow'
    assert pct_to_color(59.9) == 'orange'
    assert pct_to_color(50) == 'orange'
    assert pct_to_color(49.9) == 'red'


def test_parse_coverage_ok(tmp_path, monkeypatch):
    # Arrange
    cov_file = write_coverage(tmp_path, executed=75, missing=25)  # 75%
    monkeypatch.setattr(badge_module, 'COVERAGE_DATA', cov_file)
    # Act
    pct = badge_module.parse_coverage()
    # Assert
    assert pytest.approx(pct, rel=1e-3) == 75.0


def test_parse_coverage_missing_file(monkeypatch, tmp_path):
    # Aponta para arquivo inexistente
    missing = tmp_path / '.coverage'
    monkeypatch.setattr(badge_module, 'COVERAGE_DATA', missing)
    pct = badge_module.parse_coverage()
    assert pct == 0.0


def test_build_svg_contains_percent_and_label():
    svg = badge_module.build_svg(83.2)
    assert 'coverage' in svg
    assert '83%' in svg  # arredondado sem casas decimais
    # Verifica presença de cor (uma das hex possíveis)
    assert re.search(r"#[0-9a-f]{3,6}", svg)


def test_main_updates_badge(tmp_path, monkeypatch):
    # Usa diretório temporário para não poluir raiz
    cov_file = write_coverage(tmp_path, executed=9, missing=1)  # 90%
    monkeypatch.setattr(badge_module, 'COVERAGE_DATA', cov_file)
    badge_path = tmp_path / 'coverage-badge.svg'
    monkeypatch.setattr(badge_module, 'BADGE_FILE', badge_path)

    # Primeira execução gera arquivo
    rc1 = badge_module.main()
    assert rc1 == 0
    first_svg = badge_path.read_text()
    assert '90%' in first_svg

    # Segunda execução idempotente (não muda conteúdo)
    rc2 = badge_module.main()
    second_svg = badge_path.read_text()
    assert rc2 == 0
    assert first_svg == second_svg


def test_svg_color_mapping_examples():
    # Mapeamento esperado (replica lógica interna do script)
    color_hex = {
        'brightgreen': '4c1',
        'green': '2ea44f',
        'yellowgreen': 'a4a61d',
        'yellow': 'e3b341',
        'orange': 'fe7d37',
        'red': 'e05d44',
    }
    seen = set()
    for pct in [95, 85, 75, 65, 55, 45]:
        svg = badge_module.build_svg(pct)
        expected_color_name = badge_module.pct_to_color(pct)
        expected_hex = color_hex[expected_color_name]
        assert f"fill='#{expected_hex}'" in svg, f"Hex {expected_hex} não encontrado para {expected_color_name} ({pct}%)"
        seen.add(expected_hex)
    # Deve ter todas as 6 cores diferentes
    assert len(seen) == 6
