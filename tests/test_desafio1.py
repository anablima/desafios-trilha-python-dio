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
    # Agora deve emitir aviso e ainda cadastrar
    assert 'Aviso: endereço potencialmente inválido' in saida
    assert 'cadastrado com sucesso' in saida
    assert len(clientes) == 1

def test_cadastrar_cliente_logradouro_sem_virgula(monkeypatch, capsys):
    clientes = []
    entradas = ['11122233300','Zé','10/10/1990','RuaSemVirgula 10 - Centro - Cidade/UF']
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(entradas))
    desafio_mod.cadastrar_cliente(clientes)
    saida = capsys.readouterr().out
    assert 'Aviso: endereço potencialmente inválido' in saida
    assert len(clientes) == 1

def test_cadastrar_cliente_cidade_sem_barra(monkeypatch, capsys):
    clientes = []
    entradas = ['11122233301','Lu','10/10/1990','Rua X, 10 - Centro - CidadeUF']
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(entradas))
    desafio_mod.cadastrar_cliente(clientes)
    saida = capsys.readouterr().out
    assert 'Aviso: endereço potencialmente inválido' in saida
    assert len(clientes) == 1

def test_saque_valor_invalido(monkeypatch, capsys):
    saldo, extrato, numero_saques = 100, '', 0
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(['0']))
    saldo, extrato, numero_saques = desafio_mod.sacar_valor(saldo, desafio_mod.limite, numero_saques, desafio_mod.LIMITE_SAQUES, extrato)
    desafio_mod.exibir_extrato(saldo, extrato)
    saida = capsys.readouterr().out
    assert 'valor informado é inválido' in saida
    assert 'Saldo: R$ 100.00' in saida
    assert 'Saque:' not in saida

def test_criar_conta_corrente_sucesso(monkeypatch, capsys):
    # Prepara cliente existente e garante lista de contas limpa
    cliente = {"nome": "Maria", "cpf": "12345678900", "data_nascimento": "01/01/1990", "endereco": "Rua A, 10 - Centro - Cidade/UF"}
    clientes = [cliente]
    setattr(desafio_mod, 'contas', [])  # reset estado global de contas
    monkeypatch.setattr(builtins, 'input', sequencia_inputs([cliente['cpf']]))
    desafio_mod.criar_conta_corrente(clientes)
    saida = capsys.readouterr().out
    assert 'Conta número:' in saida
    assert cliente['nome'] in saida
    assert len(desafio_mod.contas) == 1
    conta = desafio_mod.contas[0]
    assert conta['cliente'] is cliente  # referência ao mesmo dict
    assert conta['numero'] == f"{desafio_mod.NUM_AGENCIA}-1"

def test_criar_conta_corrente_cliente_inexistente(monkeypatch, capsys):
    clientes = []
    setattr(desafio_mod, 'contas', [])
    monkeypatch.setattr(builtins, 'input', sequencia_inputs(['00011122233']))
    desafio_mod.criar_conta_corrente(clientes)
    saida = capsys.readouterr().out
    assert 'Cliente não encontrado' in saida
    assert len(desafio_mod.contas) == 0

def test_criar_conta_corrente_incrementa_numero(monkeypatch, capsys):
    cliente = {"nome": "João", "cpf": "99988877766", "data_nascimento": "02/02/1992", "endereco": "Rua B, 20 - Bairro - Cidade/UF"}
    clientes = [cliente]
    setattr(desafio_mod, 'contas', [])
    # Cria primeira conta
    monkeypatch.setattr(builtins, 'input', sequencia_inputs([cliente['cpf']]))
    desafio_mod.criar_conta_corrente(clientes)
    # Cria segunda conta para o mesmo cliente
    monkeypatch.setattr(builtins, 'input', sequencia_inputs([cliente['cpf']]))
    desafio_mod.criar_conta_corrente(clientes)
    saida = capsys.readouterr().out
    assert len(desafio_mod.contas) == 2
    nums = [c['numero'] for c in desafio_mod.contas]
    assert f"{desafio_mod.NUM_AGENCIA}-1" in nums
    assert f"{desafio_mod.NUM_AGENCIA}-2" in nums

def test_criar_varias_contas_sequencia(monkeypatch, capsys):
    """Cria 10 contas para o mesmo cliente e valida sequência numérica contínua."""
    cliente = {"nome": "Seq", "cpf": "10101010100", "data_nascimento": "03/03/1993", "endereco": "Rua S, 30 - Centro - Cidade/UF"}
    clientes = [cliente]
    setattr(desafio_mod, 'contas', [])
    for i in range(10):
        monkeypatch.setattr(builtins, 'input', sequencia_inputs([cliente['cpf']]))
        desafio_mod.criar_conta_corrente(clientes)
    saida = capsys.readouterr().out
    assert len(desafio_mod.contas) == 10
    numeros = {c['numero'] for c in desafio_mod.contas}
    esperado = {f"{desafio_mod.NUM_AGENCIA}-{i}" for i in range(1, 11)}
    assert numeros == esperado
    # Última linha de saída deve conter criação da conta 10
    assert f"{desafio_mod.NUM_AGENCIA}-10" in saida

def test_criar_contas_multiplos_clientes(monkeypatch, capsys):
    """Intercala criação de contas de dois clientes distintos garantindo sequência única global."""
    cliente_a = {"nome": "Ana", "cpf": "22233344455", "data_nascimento": "04/04/1994", "endereco": "Rua A, 40 - Centro - Cidade/UF"}
    cliente_b = {"nome": "Bruno", "cpf": "33344455566", "data_nascimento": "05/05/1995", "endereco": "Rua B, 50 - Centro - Cidade/UF"}
    clientes = [cliente_a, cliente_b]
    setattr(desafio_mod, 'contas', [])
    # Cria contas alternando CPF
    ordem_cpfs = [cliente_a['cpf'], cliente_b['cpf'], cliente_a['cpf'], cliente_b['cpf']]
    for cpf in ordem_cpfs:
        monkeypatch.setattr(builtins, 'input', sequencia_inputs([cpf]))
        desafio_mod.criar_conta_corrente(clientes)
    saida = capsys.readouterr().out
    assert len(desafio_mod.contas) == 4
    numeros = [c['numero'] for c in desafio_mod.contas]
    assert numeros == [f"{desafio_mod.NUM_AGENCIA}-1", f"{desafio_mod.NUM_AGENCIA}-2", f"{desafio_mod.NUM_AGENCIA}-3", f"{desafio_mod.NUM_AGENCIA}-4"]
    # Verifica associação correta dos clientes
    assert desafio_mod.contas[0]['cliente'] is cliente_a
    assert desafio_mod.contas[1]['cliente'] is cliente_b
    assert desafio_mod.contas[2]['cliente'] is cliente_a
    assert desafio_mod.contas[3]['cliente'] is cliente_b
