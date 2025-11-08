from test.test_reprlib import r

menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
[u] Cadastrar usuário/cliente
[c] Criar conta corrente
[l] Listar contas

=> """

# Variáveis globais
saldo = 0
limite = 500
extrato = ""
numero_saques = 0

# Constantes
LIMITE_SAQUES = 3
NUM_AGENCIA = "0001"

# Listas para armazenar clientes e contas
clientes = []
contas = []

##########################################################################
############ Administração de clientes e contas bancárias ################
##########################################################################

# Cadastro de cliente.
# Parametros: clientes (list[dict]) lista mutável onde o novo cliente será inserido.
# Regras: valida unicidade de CPF; valida formato de endereço (logradouro, número - bairro - cidade/UF).
# Retorno: None (efeitos colaterais: adiciona dict do cliente ou imprime mensagem de erro).
def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")

    # Validação de CPF simples: apenas dígitos e 11 caracteres
    cpf_digits = ''.join(filter(str.isdigit, cpf))
    if len(cpf_digits) != 11:
        print("CPF inválido!")
        return clientes
    
    # Verifica se o CPF já existe
    existente = any(
        ''.join(filter(str.isdigit, c['cpf'])) == cpf_digits
        for c in clientes
    )
    
    if existente:
        print("Já existe cliente cadastrado com esse CPF.")
        return

    nome = input("Informe o nome do cliente: ")
    dt_nascimento = input("Informe a data de nascimento do cliente (DD/MM/AAAA): ")
    endereco = input("Informe o endereço do cliente (logradouro, número - bairro - cidade/sigla estado): ")

    # Validação agora é opcional: sempre cadastra e, se formato duvidoso, emite aviso sem bloquear
    ok, aviso = validar_endereco(endereco)
    if not ok:
        print(f"Aviso: endereço potencialmente inválido ({aviso}). Cadastro prossegue.")

    cliente = {"nome": nome, "cpf": cpf, "data_nascimento": dt_nascimento, "endereco": endereco}
    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

# Criação de conta corrente.
# Parametros: clientes (list[dict]) para localizar cliente existente pelo CPF digitado.
# Regras: exige cliente pré-cadastrado; gera número sequencial global usando tamanho da lista "contas".
# Retorno: dict da conta criada ou None se cliente não encontrado. Efeitos: muta listas globais e cliente['contas'].
def criar_conta_corrente(clientes):
    # Solicita o CPF do cliente
    cpf = input("Informe o CPF do cliente: ")
    
    # Verifica se o cliente existe
    cliente = next((c for c in clientes if c["cpf"] == cpf), None)

    if not cliente:
        print("Cliente não encontrado, cadastre o cliente antes de prosseguir!")
        return 

    # Cria a conta corrente
    conta = {
        "numero": f"{NUM_AGENCIA}-{len(contas) + 1}",
        "cliente": cliente,
        "saldo": 0,
        "limite": 500,
        "extrato": "",
        "numero_saques": 0
    }

    contas.append(conta)
    print(f"Conta número: {conta['numero']} criada para o cliente {cliente['nome']}.")
    
    # Adiciona a conta à lista de contas do cliente
    if "contas" not in cliente:
        cliente["contas"] = []
    cliente["contas"].append(conta)
    return conta

# Listagem de contas.
# Parametros: contas (list[dict]) cada item contém 'numero' e 'cliente'.
# Regras: apenas imprime; não retorna estrutura; não modifica estado.
def listar_contas(contas):
    for conta in contas:
        cliente = conta["cliente"]
        print(f"Agência: {NUM_AGENCIA} | Conta: {conta['numero']} | Titular: {cliente['nome']}")


##########################################################################
####### Operações de depósito, saque e exibição de extrato bancário ######
##########################################################################

# Operação de depósito com I/O.
# Parametros: saldo (float) saldo atual; extrato (str) linhas acumuladas.
# Lê valor via input(); usa aplicar_deposito para lógica pura; em caso de erro, mantém saldo/extrato.
# Retorno: (novo_saldo, novo_extrato).
def depositar_valor(saldo, extrato):
    valor = float(input("Informe o valor do depósito: "))
    
    # Tenta aplicar o depósito e captura possíveis erros
    try:
        novo_saldo, linha = aplicar_deposito(saldo, valor)
        saldo = novo_saldo
        extrato += linha
    except ValueError:
        print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato

# Operação de saque com I/O.
# Parametros: saldo (float), limite (float), numero_saques (int), LIMITE_SAQUES (int), extrato (str).
# Lê valor via input(); delega a aplicar_saque; mantém ordem de validação: saldo->limite->nº saques->valor>0.
# Retorno: (novo_saldo, novo_extrato, numero_saques_atualizado).
def sacar_valor(saldo, limite, numero_saques, LIMITE_SAQUES, extrato):
    valor = float(input("Informe o valor do saque: "))
    
    # Tenta aplicar o saque e captura possíveis erros
    try:
        saldo, linha, numero_saques = aplicar_saque(saldo, limite, numero_saques, LIMITE_SAQUES, valor)
        extrato += linha
    except ValueError as e:
        msg = str(e)
        if msg == "saldo insuficiente":
            print("Operação falhou! Você não tem saldo suficiente.")
        elif msg == "limite excedido":
            print("Operação falhou! O valor do saque excede o limite.")
        elif msg == "limite de saques excedido":
            print("Operação falhou! Número máximo de saques excedido.")
        else:  # valor inválido
            print("Operação falhou! O valor informado é inválido.")
    return saldo, extrato, numero_saques

# Exibição de extrato.
# Parametros: saldo (float), extrato (str) acumulado.
# Regras: imprime cabeçalho, movimentações ou mensagem padrão e saldo final.
# Retorno: extrato (inalterado).
def exibir_extrato(saldo, extrato):
    
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

    return extrato

##########################################################################
######################## Funções Financeiras Brutas ######################
##########################################################################

## Função pura de depósito.
# Parametros: saldo (float) >=0; valor (float) >0.
# Regras: rejeita valor <=0 (ValueError 'valor inválido'). Não formata saldo antigo.
# Retorno: (novo_saldo, linha_extrato).
def aplicar_deposito(saldo: float, valor: float):
    """Retorna novo saldo e linha de extrato para um depósito válido.
    Levanta ValueError em caso de valor inválido (<=0).
    """
    if valor <= 0:
        raise ValueError("valor inválido")
    return saldo + valor, f"Depósito: R$ {valor:.2f}\n"

## Função pura de saque.
# Parametros: saldo (float), limite (float), numero_saques (int), LIMITE_SAQUES (int), valor (float).
# Regras: valida em ordem: excedeu saldo, excedeu limite, excedeu nº saques, valor>0; lança ValueError
# com mensagens específicas. Em sucesso decrementa saldo e incrementa contador.
# Retorno: (novo_saldo, linha_extrato, numero_saques+1).
def aplicar_saque(saldo: float, limite: float, numero_saques: int, LIMITE_SAQUES: int, valor: float):
    """Processa saque de forma bruta, retornando novo saldo, linha de extrato e contador atualizado.
    Ordem de validação preservada: saldo -> limite -> número de saques -> valor > 0.
    Levanta ValueError com mensagens específicas para cada condição violada:
    - "saldo insuficiente"
    - "limite excedido"
    - "limite de saques excedido"
    - "valor inválido"
    """
    if valor > saldo:
        raise ValueError("saldo insuficiente")
    if valor > limite:
        raise ValueError("limite excedido")
    if numero_saques >= LIMITE_SAQUES:
        raise ValueError("limite de saques excedido")
    if valor <= 0:
        raise ValueError("valor inválido")
    return saldo - valor, f"Saque: R$ {valor:.2f}\n", numero_saques + 1

##########################################################################
########################## Validação de Endereço #########################
##########################################################################

def validar_endereco(endereco: str):
    """Valida formato esperado 'logradouro, número - bairro - cidade/UF'.
    Retorna (ok: bool, detalhe: str). Não lança exceções. Aceita qualquer string e apenas sinaliza problemas.
    Critérios:
    - Deve conter exatamente 3 segmentos separados por ' - '
    - Primeiro segmento deve ter vírgula separando logradouro e número
    - Último segmento deve conter '/'
    Se qualquer critério falhar, ok=False e detalhe descreve primeira falha.
    """
    partes = endereco.split(' - ')
    if len(partes) != 3:
        return False, 'segmentação incorreta'
    logradouro_numero, _bairro, cidade_estado = partes
    if ',' not in logradouro_numero:
        return False, 'logradouro sem vírgula'
    if '/' not in cidade_estado:
        return False, 'cidade/UF sem barra'
    return True, 'válido'

#########################################################################
############################ MENU PRINCIPAL #############################
#########################################################################

if __name__ == "__main__":
    while True:
        opcao = input(menu)
        
        if opcao == "u":
            cadastrar_cliente(clientes)
        elif opcao == "c":
            criar_conta_corrente(clientes)
        elif opcao == "l":
            listar_contas(contas)
        elif opcao == "d":
            saldo, extrato = depositar_valor(saldo, extrato)
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar_valor(saldo, limite, numero_saques, LIMITE_SAQUES, extrato)
        elif opcao == "e":
            extrato = exibir_extrato(saldo, extrato)
        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
