# Desafio 1 - DIO Python

## Objetivos Geral

* Separar funções existentes em: Saque, Depósito e Extrato.
* Crias duas novas funções: Cadastrar usuário (cliente) e cadastrar conta bancária.

### Desafio

1. Separar código existente nas funções: sacar_valor, depositar_valor e exibir_extrato;
2. Criar duas novas funções: cadastrar_cliente e criar_conta_corrente, sendo que: 
   1. A função cadastrar_cliente deverá vincular cliente a uma agência do banco;
   2. A função criar_conta_corrente deverá vincular conta com cliente.

### Pré requisitos para a separação das funções

1. Cada função terá uma regra na passagem de argumentos;
2. Posso definir como será realizado o retorno e a forma como serão chamadas.

#### Saque

1. Deve receber os argumentos apenas por nome (keyword only):
   1. Sugestão de argumentos: saldo, valor, extrato, limite, numero_saques, limite_saques;
   2. Sugestão de retorno: saldo e extrato.

#### Depósito

1. Deve receber os argumentos apenas por posição (positional only):
   1. Sugestão de argumentos: saldo, valor e extrato;
   2. Sugestão de retorno: saldo e extrato.

#### Extrato

1. Deve receber os argumentos apenas por posição (positional only) e nome (keyword only):
   1. Argumentos posicionais: saldo e argumentos;
   2. Argumentos nomeados: extrato.

### Novas funções

#### Pré Requisitos - Criar usuário (cliente)

1. Armazenar usuários em uma lista;
2. Cliente possui: nome, dt_nascimento, cpf e endereco:
   1. Campo endereco é do tipo string com o formato: logradouro, nro - bairro - cidade/sigla do estado;
   2. Campo cpf é do tipo string e deve conter somente números;
   3. Não podemos cadastrar usuários com o mesmo cpf.

#### Pré Requisitos - Criar conta corrente

1. Armazenar contas em uma lista;
2. Conta possui: num_agencia, num_conta e cliente:
   1. num_conta é sequencial, iniciando em 1;
   2. num_agencia é fixo: "0001";
   3. cliente pode ter mais de uma conta, mas uma conta sempre pertencerá a somente um cliente.

##### Dica!

Para vincular um cliente/usuário a uma conta, filtre a lista de usuários burcando o número do CPF informado para cada usuário da lista.