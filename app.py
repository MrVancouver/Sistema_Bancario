import time

saldo = 0
saques_realizados = 0
extrato = []
def depositar(valor):
    global saldo, extrato
    if valor.lower() == 'q':  
        return 
    try:
        valor = float(valor)  
        if valor > 0:
            saldo += valor
            extrato.append(f"Depósito: +R$ {valor:.2f}") 
            print(f"Depósito de R${valor:.2f} realizado com sucesso!")
        else:
            print("Insira apenas valores acima de 0")
    except ValueError:
        print("Erro: Insira um valor numérico válido ou 'q' para voltar ao menu.")

def sacar(valor):
    global saldo, saques_realizados, extrato
    LIMITE_SAQUE_VALOR = 500
    LIMITE_SAQUE_VEZES = 3

    if valor.lower() == 'q':  
        return 
    try:
        valor = float(valor)  
        if saques_realizados >= LIMITE_SAQUE_VEZES:
            time.sleep(2)
            print("Limite de saques diários atingido.")
        elif valor > LIMITE_SAQUE_VALOR:
            time.sleep(2)
            print("O valor máximo de saque é de R$500.")
        elif saldo < valor:
            time.sleep(2)
            print("Seu saldo é insuficiente para o saque.")
        elif valor <= 0:
            time.sleep(2)
            print("Insira um valor apropriado para o saque.")
        else:
            saldo -= valor
            saques_realizados += 1
            extrato.append(f"Saque: -R$ {valor:.2f}")
            print(f"Saque realizado: R${valor:,.2f}")
            print(f"Você ainda tem {LIMITE_SAQUE_VEZES - saques_realizados} saques restantes hoje.")
            print(f"Seu saldo atual é: R${saldo:,.2f}")
    except ValueError:
        print("Erro: Insira um valor numérico válido ou 'q' para voltar ao menu.")

def exibir_extrato(saldo, /, *, extrato):
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in extrato:
            print(transacao)  
    
    print(f"\nSaldo:\t\tR$ {saldo:.2f}")
    print("==========================================")

def menu():
    while True:
        print(
            """
            O que deseja fazer agora?

            (S) Realizar um Saque.
            (E) Ver seu Extrato.
            (D) Fazer um Depósito.
            (X) Parar Execução.
            """
        )
        escolha = input("\nDeseja realizar qual operação?\n => ").lower()

        if escolha == 's':
            print("A qualquer momento, pressione 'q' para voltar ao menu principal.")
            time.sleep(2)
            valor_saque = input("\nIndique um valor para o Saque: ")
            time.sleep(1)
            print("Trabalhando nisso...")
            time.sleep(2)
            sacar(valor_saque)
        elif escolha == 'e':
            print("Procurando seu extrato...")
            time.sleep(1)
            exibir_extrato(saldo, extrato=extrato)
        elif escolha == 'd':
            print("A qualquer momento, pressione 'q' para voltar ao menu principal.")
            time.sleep(1)
            valor_deposito = input("\nIndique um valor para depositar na sua conta: ")
            depositar(valor_deposito)
        elif escolha == 'x':
            print("Encerrando o sistema...")
            time.sleep(1)
            print("Obrigado pela escolha!")
            break 
        else:
            print("Opção inválida! Por favor, tente novamente.")

print("Bem-vindo à página Inicial do Banco Nacional da DIO.\n")
menu()
