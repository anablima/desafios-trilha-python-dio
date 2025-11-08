# Desafios Trilha Python DIO

![CI](https://github.com/anablima/desafios-trilha-python-dio/actions/workflows/tests.yml/badge.svg) ![Coverage](coverage-badge.svg?v=78.4) Cobertura: <!--COVERAGE_PCT-->78.4%<!--/COVERAGE_PCT--> 

## Desafio 1 – Sistema Bancário Simples (Depósito, Saque e Extrato)

Este repositório contém a implementação de um pequeno sistema bancário em Python proposto na trilha da **Digital Innovation One (DIO)**. O objetivo é praticar lógica de programação, uso de funções, validação de entrada e controle de estado em memória.

## 🧠 Visão Geral

O programa executa em modo interativo via terminal, exibindo um menu com operações:

```text
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
```

Enquanto o usuário não escolhe `q`, o loop continua aceitando operações e atualizando o estado da conta.

## ✨ Funcionalidades

- Realizar depósitos (apenas valores positivos)
- Realizar saques com regras de negócio:
  - Máximo de 3 saques por execução (`LIMITE_SAQUES = 3`)
  - Limite de R$ 500,00 por saque (`limite = 500`)
  - Não permite sacar mais do que o saldo
- Exibir extrato consolidado de movimentações
- Mensagens de erro claras para operações inválidas

## 🗂️ Estrutura do Código

Toda a lógica está em `desafio-1.py`.

Principais variáveis globais:

- `saldo`: saldo atual da conta
- `limite`: limite máximo por saque (R$ 500)
- `extrato`: string acumulando transações
- `numero_saques`: contador de saques realizados
- `LIMITE_SAQUES`: constante que limita quantidade de saques (3)

Funções:

```python
def depositar_valor(saldo, extrato):
    # Lê valor, valida e atualiza saldo + extrato
    return saldo, extrato

def sacar_valor(saldo, limite, numero_saques, LIMITE_SAQUES, extrato):
    # Aplica todas as regras de saque e atualiza estado
    return saldo, extrato, numero_saques

def exibir_extrato(saldo, extrato):
    # Mostra todas as transações ou mensagem padrão
    return extrato
```

Cada função retorna os valores atualizados, que são reatribuídos no loop principal.

## ⚖️ Regras de Negócio

Depósito:

- Apenas valores maiores que zero.

Saque:

- Valor deve ser positivo.
- Não pode exceder o saldo disponível.
- Não pode exceder `limite` (R$ 500).
- Quantidade de saques limitada a `LIMITE_SAQUES` (3).

Extrato:

- Exibe cada linha formatada como `Depósito: R$ X` ou `Saque: R$ Y`.
- Caso não haja movimentações, mostra mensagem padrão.

## 🚀 Como Executar

Pré-requisito: Python 3.8+ (recomendado 3.11 ou superior).

Clone o repositório e execute:

```bash
python desafio-1.py
```

## 💻 Exemplo de Execução

```text
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
=> d
Informe o valor do depósito: 100
=> s
Informe o valor do saque: 20
=> e
================ EXTRATO ================
Depósito: R$ 100.00
Saque: R$ 20.00

Saldo: R$ 80.00
==========================================
=> q
```

## 🧪 Teste Manual Rápido

Sugestões para validar comportamentos:

1. Tentar sacar sem saldo (espera mensagem de erro de saldo insuficiente).
2. Realizar 4 saques (o 4º deve falhar por exceder limite de quantidade).
3. Sacar valor maior que 500 (falha por exceder limite).
4. Depositar valor negativo (falha por valor inválido).

<!-- seção de design original removida por duplicação; ver seção mais completa abaixo -->

## 📦 Possíveis Melhorias Futuras

- Persistência em arquivo (JSON / CSV) ou banco de dados.
- Separar lógica em módulo (`banco.py`) e manter script interativo limpo.
- Criar classe `Conta` e encapsular regras (possível uso de `dataclass`).
- Adicionar internacionalização (mensagens em múltiplos idiomas).
- Validar entradas de forma robusta (repetir prompt até valor válido).
- Suporte a múltiplas contas / usuários.
- Interface via `argparse` ou modo não interativo para automação.

## 🗂️ Estrutura do Código (Atual)

```text
desafios-trilha-python-dio/
├── desafio-1.py              # Script interativo com lógica bancária
├── scripts/
│   └── update_badge.py       # Geração de badge de cobertura
├── tests/
│   ├── test_desafio1.py      # Testes do fluxo interativo
│   └── test_update_badge.py  # Testes do gerador de badge
├── coverage-badge.svg        # Badge (gerado após testes)
└── README.md                 # Documentação
```

## 🔍 Considerações de Design

Script interativo acoplado a `input()` imprime mensagens diretamente.

- Testes do fluxo interativo usam subprocesso (arquivo com hífen dificulta importação direta).
- Script `scripts/update_badge.py` é separado e puro (apenas lê `.coverage`, gera SVG e imprime status). Facilita teste unitário.
- `extrato` mantido como string acumulada para simplicidade pedagógica.
- Evolução futura: extrair funções puras sem IO para módulo dedicado (`banco.py`) e/ou classe `Conta`.

## 📄 Licença

Este projeto está licenciado sob a licença **MIT**. Veja o arquivo `LICENSE` para o texto completo.

## 📊 Cobertura e Testes

É obrigatório executar os testes unitários em cada alteração. A cobertura mínima de linhas exigida pelo pipeline (atualmente relaxada para facilitar evolução inicial) é **15%**. Caso uma mudança reduza a cobertura abaixo desse valor, adicione testes ou refatore para restaurar o índice. Recomenda-se elevar progressivamente para 30%, 50%, 70% conforme amadurecer. O valor mais recente (atualizado automaticamente pelo CI) aparece no topo do README.

Resumo da política:

- Rodar `pytest -q` antes de commitar.
- Verificar cobertura local com: `pytest --cov=desafio-1 --cov-report=term --cov-fail-under=15 -q`.
- Cada novo recurso deve ter ao menos: cenário de sucesso + 1 cenário de erro/limite.
- Badge de cobertura é gerada localmente (sem serviços externos).
- Limiares podem ser elevados futuramente (ex.: 80%, 85%).

Rodar localmente:

```bash
pytest --cov=desafio-1 --cov-report=term --cov-fail-under=70 -q
```

Thresholds de cor da badge (linhas):

| Cobertura ≥ | Cor (nome)    | Hex      |
|-------------|---------------|----------|
| 90%         | brightgreen   | #4c1     |
| 80%         | green         | #2ea44f  |
| 70%         | yellowgreen   | #a4a61d  |
| 60%         | yellow        | #e3b341  |
| 50%         | orange        | #fe7d37  |
| <50%        | red           | #e05d44  |

O arquivo `coverage-badge.svg` só é atualizado se o conteúdo muda (idempotência).
Nota: O arquivo `coverage.xml` foi removido; a badge é gerada diretamente a partir de `.coverage`.

O projeto já possui testes automatizados em `tests/` (execução obrigatória). Política mínima atual: cobertura de linhas >= 15%.

- `test_desafio1.py`: Exercita operações de depósito, saque (limites, saldo insuficiente, exceder número de saques) e extrato usando execução do script (simulação de fluxo interativo).
- `test_update_badge.py`: Cobre lógica de geração da badge (parse de `.coverage`, faixas de cor, idempotência, formatação do SVG).

Para executar:

```bash
pytest -q
```

Com cobertura (falha se <70%):

```bash
pytest --cov=desafio-1 --cov-report=term --cov-fail-under=70 -q
```

### Próximos passos sugeridos

1. Extrair lógica bancária para módulo puro (`banco.py`) sem `input()`/`print()`, facilitando testes diretos.
2. Adicionar testes unitários puros (sem subprocess) para validar regras de negócio isoladamente.
3. Expandir cenários: múltiplos depósitos/saques em sequência, limites extremos (0, valores altos), formato do extrato.
4. Introduzir objeto `Conta` com `dataclass` para reduzir número de parâmetros.
5. Parametrizar limites (valor por saque, número de saques) via constantes ou config.

Se este repositório foi útil para seus estudos, deixe uma estrela ⭐ e compartilhe!
