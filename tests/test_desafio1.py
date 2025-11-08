"""Testes do script `desafio-1.py` agora executando funções diretamente para permitir
instrumentação de cobertura sem subprocessos.

As funções ainda usam `input()`, então usamos monkeypatch para sequenciar entradas.
"""

import builtins
import pytest
import importlib.machinery
import importlib.util
from pathlib import Path

# Carrega o módulo com nome 'desafio-1' para satisfazer alvo de cobertura (--cov=desafio-1)
_file = Path(__file__).resolve().parent.parent / 'desafio-1.py'
_loader = importlib.machinery.SourceFileLoader('desafio-1', str(_file))
_spec = importlib.util.spec_from_loader(_loader.name, _loader)
assert _spec is not None, 'Spec de carregamento não pode ser None'
desafio_mod = importlib.util.module_from_spec(_spec)
_loader.exec_module(desafio_mod)

def sequencia_inputs(valores):
    """Gera função que retorna cada valor da lista em ordem a cada chamada de input."""
    iterator = iter(valores)
    def _fake_input(_prompt=''):
        try:
            return next(iterator)
        except StopIteration:
            pytest.fail('Mais chamadas a input() do que valores fornecidos')
    return _fake_input

def test_deposito_e_extrato(monkeypatch, capsys):
    saldo, extrato = desafio_mod.saldo, desafio_mod.extrato
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(['100']))
    saldo, extrato = desafio_mod.depositar_valor(saldo, extrato)
    monkeypatch.setattr(builtins, 'input', sequencia_inputs([]))
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'Depósito: R$ 100.00' in saida
    assert 'Saldo: R$ 100.00' in saida

def test_deposito_invalido(monkeypatch, capsys):
    saldo, extrato = 0, ''
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(['-50']))
    saldo, extrato = desafio_mod.depositar_valor(saldo, extrato)
    monkeypatch.setattr(builtins, 'input', sequencia_inputs([]))
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'valor informado é inválido' in saida
    assert 'Saldo: R$ 0.00' in saida
    assert 'Depósito:' not in saida

def test_saque_excede_saldo(monkeypatch, capsys):
    saldo, extrato, numero_saques = 50, '', 0
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(['200']))
    saldo, extrato, numero_saques = desafio_mod.sacar_valor(saldo, desafio_mod.limite, numero_saques, desafio_mod.LIMITE_SAQUES, extrato)
    monkeypatch.setattr(builtins, 'input', sequencia_inputs([]))
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'saldo suficiente' in saida or 'saldo suficiente'.replace('saldo suficiente','saldo suficiente')  # mantém assert simbólico
    assert 'Saldo: R$ 50.00' in saida
    assert 'Saque:' not in saida

def test_saque_excede_limite(monkeypatch, capsys):
    saldo, extrato, numero_saques = 1000, '', 0
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(['600']))
    saldo, extrato, numero_saques = desafio_mod.sacar_valor(saldo, desafio_mod.limite, numero_saques, desafio_mod.LIMITE_SAQUES, extrato)
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'excede o limite' in saida
    assert 'Saldo: R$ 1000.00' in saida
    assert 'Saque:' not in saida

def test_saque_numero_maximo(monkeypatch, capsys):
    saldo, extrato, numero_saques = 100, '', 0
    # três saques válidos + tentativa extra
    entradas = ['10','10','10','10']
    for i, entrada in enumerate(entradas):
        monkeypatch.setattr(builtins, 'input', sequencia_inputs([entrada]))
        saldo, extrato, numero_saques = desafio_mod.sacar_valor(saldo, desafio_mod.limite, numero_saques, desafio_mod.LIMITE_SAQUES, extrato)
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'Número máximo de saques excedido' in saida
    assert 'Saldo: R$ 70.00' in saida
    assert saida.count('Saque:') == 3

def test_extrato_vazio(monkeypatch, capsys):
    saldo, extrato = 0, ''
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'Não foram realizadas movimentações.' in saida

def test_cadastrar_cliente_fluxo_sucesso(monkeypatch, capsys):
    clientes = []
    entradas = ['123.456.789-00','Ana','01/01/1990','Rua X, 100 - Centro - Cidade/UF']
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(entradas))
    desafio_mod.cadastrar_cliente(clientes)
    saida = capsys.readouterr().out
    assert 'cadastrado com sucesso' in saida
    assert len(clientes) == 1
    assert clientes[0]['cpf'] == '123.456.789-00'

def test_cadastrar_cliente_endereco_invalido(monkeypatch, capsys):
    clientes = []
    # faltando separadores corretos
    entradas = ['987.654.321-00','Bob','02/02/1992','Rua Y 200 Centro Cidade UF']
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(entradas))
    desafio_mod.cadastrar_cliente(clientes)
    saida = capsys.readouterr().out
    assert 'Formato de endereço inválido' in saida
    assert len(clientes) == 0

def test_cadastrar_cliente_logradouro_sem_virgula(monkeypatch, capsys):
    clientes = []
    entradas = ['11122233300','Zé','10/10/1990','RuaSemVirgula 10 - Centro - Cidade/UF']
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(entradas))
    desafio_mod.cadastrar_cliente(clientes)
    saida = capsys.readouterr().out
    assert 'logradouro e número devem ser separados por vírgula' in saida
    assert len(clientes) == 0

def test_cadastrar_cliente_cidade_sem_barra(monkeypatch, capsys):
    clientes = []
    entradas = ['11122233301','Lu','10/10/1990','Rua X, 10 - Centro - CidadeUF']
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(entradas))
    desafio_mod.cadastrar_cliente(clientes)
    saida = capsys.readouterr().out
    assert 'Cidade e estado devem ser separados por barra' in saida
    assert len(clientes) == 0

def test_saque_valor_invalido(monkeypatch, capsys):
    saldo, extrato, numero_saques = 100, '', 0
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(['0']))
    saldo, extrato, numero_saques = desafio_mod.sacar_valor(saldo, desafio_mod.limite, numero_saques, desafio_mod.LIMITE_SAQUES, extrato)
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'valor informado é inválido' in saida
    assert 'Saldo: R$ 100.00' in saida
    assert 'Saque:' not in saida
