# Guia para Agentes – desafios-trilha-python-dio

## Panorama Atual
Projeto educacional de sistema bancário simples. Toda a lógica hoje está concentrada em `desafio-1.py` (funções ainda fazem I/O direto). Scripts auxiliares em `scripts/` geram e propagam badge de cobertura. Testes em `tests/` usam `monkeypatch` sobre `input()` e captura de saída (`capsys`). O arquivo fazia referência a um módulo `banco.py` que NÃO existe (planejado como evolução futura).

## Arquitetura & Componentes
* `desafio-1.py`: estado global (saldo, limite, extrato, numero_saques, clientes) + funções: `depositar_valor`, `sacar_valor`, `exibir_extrato`, `cadastrar_cliente`.
* `scripts/update_badge.py`: gera `coverage-badge.svg` lendo `.coverage`; idempotente; mapeia faixas de cor (>=90 brightgreen ... <50 red).
* `scripts/update_readme_coverage.py`: substitui placeholder `<!--COVERAGE_PCT-->X%<!--/COVERAGE_PCT-->` e adiciona `?v=NN.N` à imagem para cache-bust.
* `tests/`: carregam módulos via `SourceFileLoader` (nome com hífen) e usam funções diretamente; evitam subprocess.

## Padrões Específicos
* Import dinâmico: para cobrir `desafio-1.py` usa `importlib.machinery.SourceFileLoader('desafio-1', path)`.
* Testes simulam sequência de inputs com gerador (`sequencia_inputs`). Falha se chamadas excedem valores preparados.
* `extrato`: string acumulada com linhas `Depósito: R$ X.YZ` / `Saque: R$ X.YZ`; extrato vazio imprime mensagem padrão.
* Validações de saque: ordem de checagem (saldo → limite → número de saques → valor > 0). Primeiro motivo bloqueia operação.
* Cadastro de cliente: valida formato do endereço `logradouro, número - bairro - cidade/UF` e unicidade de CPF.

## Fluxos de Trabalho
* Testes rápidos: `pytest -q`.
* Cobertura local: `pytest --cov=desafio-1 --cov-report=term -q` (mínimo atual esperado >=15%).
* Atualizar badge: executar `python scripts/update_badge.py` (CI já faz; só grava se mudou).
* Propagar percentual no README: `python scripts/update_readme_coverage.py` (requer placeholder existente).

## Convenções ao Evoluir
* Antes de refatorar para pureza, manter interface compatível: funções retornam estado atualizado (ex.: saque retorna `saldo, extrato, numero_saques`).
* Novas operações: seguir estilo `def operacao(param_estado..., input?)->(novo_estado...)`; ideal futuro é remover `input()/print()` e delegar ao script interativo.
* Manter idempotência em scripts de automação (gravar arquivo só se conteúdo difere).
* Ao adicionar função pura, criar testes sem `monkeypatch` e gradualmente migrar lógica de I/O para camada externa.

## Edge Cases a Cobrir em Novos Testes
* Depósito/saque com valor 0 ou negativo.
* Saque exatamente no limite (500) e exatamente no saldo.
* Quarto saque excedendo `LIMITE_SAQUES`.
* Extrato após mistura de depósitos/saques (contagem precisa de linhas).
* Cliente duplicado pelo mesmo CPF e formatos de endereço inválidos (faltando vírgula ou barra).

## Próxima Evolução Recomendada
Extrair módulo `banco.py` com funções puras sem I/O; adaptar testes para chamar diretamente sem `monkeypatch`; depois encapsular estado em `dataclass Conta`.

---
Se algo acima estiver impreciso ou faltar detalhe (ex.: política exata de aumento de cobertura), peça atualização e descreva o cenário desejado.