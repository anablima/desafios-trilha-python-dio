import importlib.machinery
import importlib.util
from pathlib import Path
import re

README_TMP = Path('README.md')
SCRIPT_PATH = Path('scripts/update_readme_coverage.py')

# Carrega o módulo dinamicamente
_loader = importlib.machinery.SourceFileLoader('scripts.update_readme_coverage', str(SCRIPT_PATH))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
assert _spec is not None
mod = importlib.util.module_from_spec(_spec)
_loader.exec_module(mod)


def write_readme(content: str):
    README_TMP.write_text(content, encoding='utf-8')


def test_update_readme_basic(tmp_path, monkeypatch):
    # Usa diretório temporário para isolar
    monkeypatch.chdir(tmp_path)
    # Criar README com placeholder
    write_readme('![Coverage](coverage-badge.svg) Cobertura atual: <!--COVERAGE_PCT-->0%<!--/COVERAGE_PCT-->\n')
    # Força valor de cobertura
    monkeypatch.setattr(mod, 'read_pct_from_api', lambda: 82.94)
    monkeypatch.setattr(mod, 'read_pct_from_badge', lambda: None)
    result = mod.update_readme()
    assert result is True
    updated = README_TMP.read_text(encoding='utf-8')
    assert '82.9%' in updated  # arredondado uma casa
    assert '?v=82.9)' in updated


def test_update_readme_no_placeholder(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_readme('Sem marcador de cobertura aqui.')
    monkeypatch.setattr(mod, 'read_pct_from_api', lambda: 50.0)
    r = mod.update_readme()
    assert r is False
    assert '50.0%' not in README_TMP.read_text(encoding='utf-8')


def test_update_readme_idempotent(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_readme('![Coverage](coverage-badge.svg?v=75.0) Cobertura atual: <!--COVERAGE_PCT-->75.0%<!--/COVERAGE_PCT-->\n')
    monkeypatch.setattr(mod, 'read_pct_from_api', lambda: 75.0)
    r = mod.update_readme()
    assert r is False  # nada muda
    txt = README_TMP.read_text(encoding='utf-8')
    assert txt.count('75.0%') == 1


def test_update_readme_fallback_badge(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    write_readme('![Coverage](coverage-badge.svg) Cobertura atual: <!--COVERAGE_PCT-->0%<!--/COVERAGE_PCT-->\n')
    # Simula falha na API e badge com número
    monkeypatch.setattr(mod, 'read_pct_from_api', lambda: None)
    monkeypatch.setattr(mod, 'read_pct_from_badge', lambda: 61.0)
    r = mod.update_readme()
    assert r is True
    txt = README_TMP.read_text(encoding='utf-8')
    assert '61.0%' in txt
    assert '?v=61.0)' in txt
