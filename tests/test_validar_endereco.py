"""Testes puros para validar_endereco em desafio-1.py"""
import importlib.machinery
import importlib.util
from pathlib import Path

_file = Path(__file__).resolve().parent.parent / 'desafio-1.py'
_loader = importlib.machinery.SourceFileLoader('desafio-1', str(_file))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
assert _spec is not None
mod = importlib.util.module_from_spec(_spec)
_loader.exec_module(mod)


def test_validar_endereco_valido():
    ok, detalhe = mod.validar_endereco('Rua X, 100 - Centro - Cidade/UF')
    assert ok is True
    assert detalhe == 'válido'


def test_validar_endereco_segmentacao_incorreta():
    ok, detalhe = mod.validar_endereco('Rua Y, 200 Centro Cidade UF')
    assert ok is False
    assert detalhe == 'segmentação incorreta'


def test_validar_endereco_logradouro_sem_virgula():
    ok, detalhe = mod.validar_endereco('RuaSemVirgula 10 - Centro - Cidade/UF')
    assert ok is False
    assert detalhe == 'logradouro sem vírgula'


def test_validar_endereco_cidade_sem_barra():
    ok, detalhe = mod.validar_endereco('Rua Z, 10 - Centro - CidadeUF')
    assert ok is False
    assert detalhe == 'cidade/UF sem barra'
