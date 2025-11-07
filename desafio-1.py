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
LIMITE_SAQUES = 3

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
