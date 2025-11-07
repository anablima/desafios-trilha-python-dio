import sys
import subprocess
from pathlib import Path
import pytest

SCRIPT_PATH = Path(__file__).resolve().parent.parent / 'desafio-1.py'


def run_script(inputs: str):
    """Executa o script interativo passando sequência de entradas e retorna stdout."""
    result = subprocess.run([sys.executable, str(SCRIPT_PATH)], input=inputs, text=True, capture_output=True, timeout=3)
    return result.stdout


def test_fluxo_deposito_extrato():
    saida = run_script('d\n100\ne\nq\n')
    assert 'Depósito: R$ 100.00' in saida
    assert 'Saldo: R$ 100.00' in saida


@pytest.mark.parametrize(
    "entrada, mensagem_esperada, saldo_final, extrato_vazio",
    [
        ("e\nq\n", "Não foram realizadas movimentações.", "Saldo: R$ 0.00", True),
        ("d\n-50\ne\nq\n", "valor informado é inválido", "Saldo: R$ 0.00", True),
        ("s\n0\ne\nq\n", "valor informado é inválido", "Saldo: R$ 0.00", True),
    ("d\n50\ns\n200\ne\nq\n", "saldo suficiente", "Saldo: R$ 50.00", False),
        ("d\n1000\ns\n600\ne\nq\n", "excede o limite", "Saldo: R$ 1000.00", False),
        ("d\n100\ns\n10\ns\n10\ns\n10\ns\n10\ne\nq\n", "Número máximo de saques excedido", "Saldo: R$ 70.00", False),
    ],
)
def test_cenarios_erro_e_limites(entrada, mensagem_esperada, saldo_final, extrato_vazio):
    saida = run_script(entrada)
    assert mensagem_esperada in saida
    assert saldo_final in saida
    if extrato_vazio:
        assert "Não foram realizadas movimentações." in saida
    else:
        # quando não é extrato vazio, deve haver ao menos uma operação (Depósito ou Saque)
        assert any(token in saida for token in ["Depósito:", "Saque:"])
