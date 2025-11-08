menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

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

# Operação de depósito
def depositar_valor(saldo, extrato):
    
    valor = float(input("Informe o valor do depósito: "))

    if valor > 0:
        saldo += valor
        extrato += f"Depósito: R$ {valor:.2f}\n"

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato

# Operação de saque
def sacar_valor(saldo, limite, numero_saques, LIMITE_SAQUES, extrato):
    
    valor = float(input("Informe o valor do saque: "))
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")

    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")

    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")

    elif valor > 0:
        saldo -= valor
        extrato += f"Saque: R$ {valor:.2f}\n"
        numero_saques += 1

    else:
        print("Operação falhou! O valor informado é inválido.")

    return saldo, extrato, numero_saques

# Operação de exibição de extrato
def exibir_extrato(saldo, extrato):
    
    print("\n================ EXTRATO ================")
    print("Não foram realizadas movimentações." if not extrato else extrato)
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")

    return extrato

if __name__ == "__main__":
    while True:
        opcao = input(menu)
        
        if opcao == "d":
            saldo, extrato = depositar_valor(saldo, extrato)
            
        elif opcao == "s":
            saldo, extrato, numero_saques = sacar_valor(saldo, limite, numero_saques, LIMITE_SAQUES, extrato)
        
        elif opcao == "e":
            extrato = exibir_extrato(saldo, extrato)

        elif opcao == "q":
            break

        else:
            print("Operação inválida, por favor selecione novamente a operação desejada.")
