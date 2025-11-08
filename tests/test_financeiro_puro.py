"""Testes das funções puras aplicar_deposito e aplicar_saque em `desafio-1.py`.
Não utilizam monkeypatch pois não há I/O interno nestas funções.
"""
import importlib.machinery
import importlib.util
from pathlib import Path
import pytest

_file = Path(__file__).resolve().parent.parent / 'desafio-1.py'
_loader = importlib.machinery.SourceFileLoader('desafio-1', str(_file))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
assert _spec is not None
mod = importlib.util.module_from_spec(_spec)
_loader.exec_module(mod)

# Depósito
def test_aplicar_deposito_valido():
    saldo, linha = mod.aplicar_deposito(100.0, 50.0)
    assert saldo == 150.0
    assert linha.startswith('Depósito: R$ 50.00')

@pytest.mark.parametrize('valor', [0, -1, -100.5])
def test_aplicar_deposito_invalido(valor):
    with pytest.raises(ValueError) as exc:
        mod.aplicar_deposito(0.0, valor)
    assert str(exc.value) == 'valor inválido'

# Saque - sucesso
def test_aplicar_saque_valido():
    saldo, linha, n = mod.aplicar_saque(200.0, 500.0, 0, 3, 80.0)
    assert saldo == 120.0
    assert 'Saque: R$ 80.00' in linha
    assert n == 1

# Saque - validações na ordem
def test_aplicar_saque_excede_saldo():
    with pytest.raises(ValueError) as exc:
        mod.aplicar_saque(50.0, 500.0, 0, 3, 100.0)
    assert str(exc.value) == 'saldo insuficiente'

def test_aplicar_saque_excede_limite():
    with pytest.raises(ValueError) as exc:
        mod.aplicar_saque(600.0, 500.0, 0, 3, 550.0)
    assert str(exc.value) == 'limite excedido'

def test_aplicar_saque_excede_numero():
    with pytest.raises(ValueError) as exc:
        mod.aplicar_saque(600.0, 500.0, 3, 3, 10.0)
    assert str(exc.value) == 'limite de saques excedido'

@pytest.mark.parametrize('valor', [0, -10])
def test_aplicar_saque_valor_invalido(valor):
    with pytest.raises(ValueError) as exc:
        mod.aplicar_saque(600.0, 500.0, 0, 3, valor)
    assert str(exc.value) == 'valor inválido'
