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

# Função para cadastrar cliente
def cadastrar_cliente(clientes):
    cpf = input("Informe o CPF do cliente: ")
    
    # Verifica se o CPF já está cadastrado
    valida_cpf = [cliente for cliente in clientes if cliente["cpf"] == cpf]
    
    # Verifica se o CPF já está cadastrado, remove pontuação e mantém apenas dígitos
    valida_cpf_string = ''.join(filter(str.isdigit, valida_cpf[0]["cpf"])) if valida_cpf else None

    if valida_cpf_string:
        print("Já existe cliente cadastrado com esse CPF.")
        return
    
    nome = input("Informe o nome do cliente: ")
    dt_nascimento = input("Informe a data de nascimento do cliente (DD/MM/AAAA): ")
    endereco = input("Informe o endereço do cliente (logradouro, número - bairro - cidade/sigla estado): ")

    # Validar formato do endereço: logradouro, número - bairro - cidade/sigla estado
    partes_endereco = endereco.split(' - ')
    if len(partes_endereco) != 3:
        print("Formato de endereço inválido. Use: logradouro, número - bairro - cidade/sigla estado")
        return
    
    logradouro_numero = partes_endereco[0]
    bairro = partes_endereco[1]
    cidade_estado = partes_endereco[2]
    
    # Valida se logradouro contém vírgula (separa logradouro do número)
    if ',' not in logradouro_numero:
        print("Formato de endereço inválido. O logradouro e número devem ser separados por vírgula.")
        return
    
    # Valida se cidade/estado contém barra
    if '/' not in cidade_estado:
        print("Formato de endereço inválido. Cidade e estado devem ser separados por barra (/).")
        return
    
    cliente = {"nome": nome, "cpf": cpf, "data_nascimento": dt_nascimento, "endereco": endereco}

    clientes.append(cliente)
    print("Cliente cadastrado com sucesso!")

# Função criar conta
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

# Função listar contas
def listar_contas(contas):
    for conta in contas:
        cliente = conta["cliente"]
        print(f"Agência: {NUM_AGENCIA} | Conta: {conta['numero']} | Titular: {cliente['nome']}")


##########################################################################
####### Operações de depósito, saque e exibição de extrato bancário ######
##########################################################################

# Operação de depósito
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

# Operação de saque
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

# Operação de exibição de extrato
def exibir_extrato(saldo, extrato):
    
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

    return extrato

##########################################################################
######################## Funções Financeiras Brutas ######################
##########################################################################

def aplicar_deposito(saldo: float, valor: float):
    """Retorna novo saldo e linha de extrato para um depósito válido.
    Levanta ValueError em caso de valor inválido (<=0).
    """
    if valor <= 0:
        raise ValueError("valor inválido")
    return saldo + valor, f"Depósito: R$ {valor:.2f}\n"

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
