# Menu apresentado ao usuário com as opções disponíveis.
# Usa string multilinha para manter o layout legível no console.
menu = """

[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair

=> """

# Variável que guarda o saldo atual da conta (inicia em 0).
saldo = 0

# Limite máximo por saque.
limite = 500

# String que acumula o histórico de transações (extrato).
extrato = ""

# Contador de quantos saques já foram realizados na sessão.
numero_saques = 0

# Constante que define o número máximo de saques permitidos.
LIMITE_SAQUES = 3

def depositar_valor(saldo, extrato):
    # Solicita ao usuário o valor do depósito e converte para float.
    try:
        valor = float(input("Informe o valor do depósito: "))
    except ValueError:
        print("Operação falhou! Valor inválido.")
        return saldo, extrato

    # Se o valor for positivo, adiciona ao saldo e registra no extrato local.
    if valor > 0:
        # Soma o valor depositado ao saldo local e atualiza o extrato.
        saldo += valor
        extrato = extrato + f"Depósito: R$ {valor:.2f}\n"
        return saldo, extrato

    # Se o valor informado não for válido (zero ou negativo), informa o usuário.
    else:
        print("Operação falhou! O valor informado é inválido.")

def sacar_valor(saldo, extrato):
    # Solicita ao usuário o valor que deseja sacar e converte para float.
    try:
        valor = float(input("Informe o valor do saque: "))
    except ValueError:
        print("Operação falhou! Valor inválido.")
        return saldo, extrato

    # Verifica se o valor solicitado é maior que o saldo disponível.
    excedeu_saldo = valor > saldo

    # Verifica se o valor solicitado excede o limite por saque.
    excedeu_limite = valor > limite

    # Indica que a função irá acessar/modificar a variável global numero_saques.
    global numero_saques

    # Verifica se já atingimos o número máximo de saques permitidos.
    excedeu_saques = numero_saques >= LIMITE_SAQUES

    # Se não houver saldo suficiente, informa o usuário.
    if excedeu_saldo:
        print("Operação falhou! Você não tem saldo suficiente.")
        return saldo, extrato

    # Se o valor for maior do que o limite por saque, informa o usuário.
    elif excedeu_limite:
        print("Operação falhou! O valor do saque excede o limite.")
        return saldo, extrato

    # Se já tiver sido atingido o número máximo de saques, informa o usuário.
    elif excedeu_saques:
        print("Operação falhou! Número máximo de saques excedido.")
        return saldo, extrato

    # Se o valor for positivo e não houver bloqueios anteriores, realiza o saque.
    elif valor > 0:
        # Subtrai o valor sacado do saldo local e atualiza o extrato.
        saldo -= valor
        extrato = extrato + f"Saque: R$ {valor:.2f}\n"
        # Incremento do contador de saques antes de retornar.
        numero_saques += 1
        return saldo, extrato

    # Se o valor informado não for positivo, informa o usuário.
    else:
        print("Operação falhou! O valor informado é inválido.")
        return saldo, extrato
        print("Operação falhou! O valor informado é inválido.")

def exibir_extrato(extrato, saldo):
    # Imprime o cabeçalho do extrato.
    print("\n================ EXTRATO ================")

    # Se não houver movimentações registradas no extrato, informa que nada foi
    # realizado; caso contrário, mostra as linhas acumuladas do extrato.
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        print(extrato)

    # Mostra o saldo atual formatado com duas casas decimais.
    print(f"\nSaldo: R$ {saldo:.2f}")
    print("==========================================")


# Loop principal da aplicação — roda até o usuário escolher sair (opção 'q').
while True:
    opcao = input(menu).lower()

    # Se o usuário escolher 'd', chama a função de depósito.
    # Nota: agora a função retorna os valores atualizados e precisamos reatribuir.
    if opcao == "d":
        saldo, extrato = depositar_valor(saldo, extrato)

    # Se o usuário escolher 's', chama a função de saque.
    # Observação semelhante: a função retorna os valores atualizados e precisamos reatribuir.
    elif opcao == "s":
        saldo, extrato = sacar_valor(saldo, extrato)

    # Se o usuário escolher 'e', exibe o extrato e o saldo atual.
    elif opcao == "e":
        exibir_extrato(extrato, saldo)

    # Se o usuário escolher 'q', interrompe o loop e encerra o programa.
    elif opcao == "q":
        break

    # Para qualquer outra entrada, informa que a operação é inválida.
    else:
        print("Operação inválida, por favor selecione novamente a operação desejada.")


# Resumo da lógica utilizada neste desafio:
# - O programa apresenta um menu interativo com opções de depósito, saque, extrato e sair.
# - Existem variáveis globais que representam o saldo, o limite por saque, o extrato
#   (como string) e o contador de saques.
# - As funções `depositar_valor` e `sacar_valor` solicitam valores ao usuário e
#   realizam validações básicas (valor positivo, limite de saque, saldo disponível).
# - A função `exibir_extrato` imprime o histórico de transações e o saldo atual.
# - Observações importantes sobre o comportamento atual do código:
#   * As funções manipulam variáveis locais (`saldo` e `extrato`) e, na forma
#     atual, nem sempre retornam os valores atualizados ao escopo chamador.
#   * Em `sacar_valor`, há um `return` que acontece antes do incremento de
#     `numero_saques`, portanto o contador de saques não será atualizado como
#     esperado quando o saque for bem-sucedido.
#   * Para que o programa atualize corretamente o saldo/extrato, as funções
#     deveriam retornar os valores modificados e o loop principal deveria
#     reatribuir `saldo, extrato = depositar_valor(saldo, extrato)` (ou usar
#     variáveis globais de forma controlada).

