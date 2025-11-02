"""Aplicação bancária simples (versão expandida)
Objetivo: demonstrar operações de um banco fictício (depósito, saque, extrato) e agora
          incluir cadastro de clientes e contas, além de listagem.

Instruções: O código foi escrito de forma didática, comentado linha a linha.
"""

# ========================= SEÇÃO: CONSTANTES E ESTADO GLOBAL =========================

MENU = """\n\n""" \
    "[d] Depositar\n" \
    "[s] Sacar\n" \
    "[e] Extrato\n" \
    "[nc] Nova Conta\n" \
    "[lc] Listar Contas\n" \
    "[nu] Novo Cliente\n" \
    "[lu] Listar Clientes\n" \
    "[q] Sair\n\n" \
    "=> "  # String multilinha de menu, concatenada para evitar indentação acidental.

LIMITE_SAQUES = 3              # Número máximo de saques por conta/sessão.
LIMITE_VALOR_SAQUE = 500       # Limite monetário por saque.

saldo = 0.0                    # Saldo inicial da conta padrão (modo simples).
extrato = []                   # Extrato armazenado como lista de strings (mais flexível que única string).
numero_saques = 0              # Contador de saques realizados na sessão.

clientes = []                  # Lista de dicionários representando clientes.
contas = []                    # Lista de dicionários representando contas bancárias.
AGENCIA_PADRAO = "0001"        # Código fixo de agência para contas criadas.

# ========================= SEÇÃO: FUNÇÕES UTILITÁRIAS =========================

def encontrar_cliente_por_cpf(cpf):  # Recebe uma string de CPF sem formatação.
    """Retorna o dicionário do cliente se existir, senão None."""
    for cliente in clientes:             # Percorre a lista global de clientes.
        if cliente["cpf"] == cpf:       # Compara o CPF fornecido com o armazenado.
            return cliente              # Se bater, retorna o cliente.
    return None                         # Caso nenhum cliente corresponda, retorna None.

# ========================= SEÇÃO: OPERAÇÕES FINANCEIRAS =========================

def depositar_valor():  # Não recebe saldo diretamente: usa variável global para simplicidade didática.
    global saldo                     # Indica que vamos modificar o saldo global.
    # Solicita entrada do usuário para o depósito.
    valor_str = input("Informe o valor do depósito: ")
    try:                              # Tenta converter para float.
        valor = float(valor_str)
    except ValueError:                # Se falhar a conversão, trata erro.
        print("Operação falhou! Valor inválido.")
        return                        # Sai sem alterar estado.
    if valor <= 0:                    # Validação de valor positivo.
        print("Operação falhou! O valor deve ser positivo.")
        return                        # Não continua se inválido.
    saldo += valor                    # Atualiza saldo somando o depósito.
    extrato.append(f"Depósito: R$ {valor:.2f}")  # Registra a linha no extrato.
    print(f"Depósito realizado com sucesso. Saldo atual: R$ {saldo:.2f}")  # Feedback.

def sacar_valor():  # Função de saque usando estado global simplificado.
    global saldo, numero_saques       # Vamos alterar saldo e contador de saques.
    if numero_saques >= LIMITE_SAQUES:  # Verifica se atingiu limite de saques.
        print("Operação falhou! Limite de saques atingido.")
        return                        # Interrompe execução.
    valor_str = input("Informe o valor do saque: ")  # Solicita valor.
    try:                              # Conversão para float.
        valor = float(valor_str)
    except ValueError:                # Erro de conversão.
        print("Operação falhou! Valor inválido.")
        return
    if valor <= 0:                    # Validação de valor positivo.
        print("Operação falhou! Valor precisa ser positivo.")
        return
    if valor > saldo:                 # Conferência de saldo suficiente.
        print("Operação falhou! Saldo insuficiente.")
        return
    if valor > LIMITE_VALOR_SAQUE:    # Checa limite monetário por saque.
        print("Operação falhou! Valor excede limite por saque.")
        return
    saldo -= valor                    # Debita do saldo.
    numero_saques += 1                # Incrementa contador de saques.
    extrato.append(f"Saque:    R$ {valor:.2f}")  # Registra no extrato.
    print(f"Saque realizado. Saldo atual: R$ {saldo:.2f}")  # Mensagem de sucesso.

def exibir_extrato():  # Mostra extrato formatado.
    print("\n================ EXTRATO ================")  # Cabeçalho visual.
    if not extrato:                     # Verifica se lista está vazia.
        print("Não foram realizadas movimentações.")  # Mensagem de ausência.
    else:                               # Caso haja lançamentos.
        for linha in extrato:           # Percorre cada linha registrada.
            print(linha)                # Imprime a linha.
    print(f"\nSaldo: R$ {saldo:.2f}")            # Mostra saldo final.
    print("==========================================")  # Rodapé visual.

# ========================= SEÇÃO: OPERAÇÕES DE CLIENTE E CONTA =========================

def cadastrar_cliente():  # Captura dados de um novo cliente e armazena.
    cpf = input("Informe CPF (somente números): ").strip()  # Lê CPF sem formatação.
    if encontrar_cliente_por_cpf(cpf):                       # Verifica duplicidade.
        print("Já existe cliente com esse CPF.")            # Informa duplicidade.
        return                                              # Cancela cadastro.
    nome = input("Nome completo: ").strip()                 # Captura nome.
    data_nascimento = input("Data de nascimento (DD/MM/AAAA): ").strip()  # Data.
    endereco = input("Endereço (Logradouro, Nº - Bairro - Cidade/UF): ").strip()  # Endereço completo.
    clientes.append({               # Insere dicionário representando o cliente.
        "cpf": cpf,
        "nome": nome,
        "data_nascimento": data_nascimento,
        "endereco": endereco,
    })
    print("Cliente cadastrado com sucesso.")              # Confirmação.

def cadastrar_conta():  # Cria uma conta vinculada a um cliente existente.
    cpf = input("Informe o CPF do titular: ").strip()    # Solicita CPF.
    cliente = encontrar_cliente_por_cpf(cpf)              # Pesquisa cliente.
    if not cliente:                                       # Se não achar.
        print("Cliente não encontrado. Cadastre o cliente primeiro.")
        return
    numero_conta = len(contas) + 1                        # Gera número sequencial simples.
    conta = {                                             # Monta dicionário da conta.
        "agencia": AGENCIA_PADRAO,
        "numero": f"{numero_conta:04d}",                # Formata com zeros à esquerda.
        "titular_cpf": cpf,
    }
    contas.append(conta)                                  # Armazena conta.
    print(f"Conta criada com sucesso. Agência {conta['agencia']} Conta {conta['numero']}")

def listar_clientes():  # Lista clientes cadastrados.
    if not clientes:                          # Verifica lista vazia.
        print("Nenhum cliente cadastrado.")   # Mensagem se vazio.
        return
    print("\n====== CLIENTES ======")             # Cabeçalho.
    for c in clientes:                        # Itera sobre cada cliente.
        print(f"CPF: {c['cpf']} | Nome: {c['nome']} | Nasc.: {c['data_nascimento']} | End.: {c['endereco']}")

def listar_contas():  # Lista contas existentes.
    if not contas:                             # Se lista vazia.
        print("Nenhuma conta cadastrada.")    # Mensagem.
        return
    print("\n====== CONTAS ======")                # Cabeçalho.
    for conta in contas:                      # Itera contas.
        # Busca cliente relacionado para exibir nome.
        cliente = encontrar_cliente_por_cpf(conta['titular_cpf'])
        nome = cliente['nome'] if cliente else 'DESCONHECIDO'
        print(f"Agência: {conta['agencia']} | Conta: {conta['numero']} | Titular: {nome} ({conta['titular_cpf']})")

# ========================= SEÇÃO: LOOP PRINCIPAL =========================

def loop_principal():  # Controla fluxo interativo do programa.
    while True:                                      # Loop infinito até saída explícita.
        opcao = input(MENU).strip().lower()          # Lê opção do usuário, normaliza.
        if opcao == 'd':                             # Caso seja depósito.
            depositar_valor()                        # Chama função de depósito.
        elif opcao == 's':                           # Caso seja saque.
            sacar_valor()                            # Executa saque.
        elif opcao == 'e':                           # Caso seja extrato.
            exibir_extrato()                         # Exibe extrato.
        elif opcao == 'nu':                          # Novo cliente.
            cadastrar_cliente()                      # Chama cadastro cliente.
        elif opcao == 'nc':                          # Nova conta bancária.
            cadastrar_conta()                        # Cria conta.
        elif opcao == 'lu':                          # Listar clientes.
            listar_clientes()                        # Mostra clientes.
        elif opcao == 'lc':                          # Listar contas.
            listar_contas()                          # Mostra contas.
        elif opcao == 'q':                           # Sair do programa.
            print("Encerrando... Obrigado por utilizar o sistema.")  # Mensagem final.
            break                                    # Encerra o loop.
        else:                                        # Qualquer outra entrada.
            print("Opção inválida. Tente novamente.") # Feedback de erro.

# Execução automática se arquivo for executado diretamente.
if __name__ == '__main__':  # Ponto de entrada convencional.
    loop_principal()        # Inicia a interação com o usuário.
