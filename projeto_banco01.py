menu = """

[1] Depositar
[2] Sacar
[3] Extrato
[0] Sair

=>"""

saldo = 0
limite = 500
Extrato = ""
numero_saques = 0
LIMITES_SAQUES = 3

while True:
    Opcao = input(menu)
    if Opcao == "1":
        valor = float(input("Informe o valor de deposito: "))

        if valor > 0:
            saldo += valor
            Extrato += f"Deposito: R${valor:.2f}\n"

        else:
            print("operação falhou, o valor informado é inválido!.")    

    elif Opcao == "2":
        valor = float(input("informe o valor do saque:"))

        excedeu_saldo = valor > saldo
        excedeu_limite = valor > limite
        excedeu_saques = numero_saques >= LIMITES_SAQUES


        if excedeu_saldo:
            print("falha na operação, saldo insuficiente!.")

        elif excedeu_limite:
            print("falha na operação, o valor do saque é maior que o limite!.")

        elif excedeu_saques:
            print("falha na operação, limite toral de saques excedido!.")

        elif valor > 0:
            saldo -= valor
            Extrato += f"saque: R${valor:.2f}\n"
            numero_saques += 1

        else:
            print("falha na operação, o valor informado é inválido")    


    elif Opcao == "3":
        print("\n=================Extrato=================")    
        print("não foram realizadas movimentaçoes." if not Extrato else Extrato)
        print(f"\nsaldo: R${saldo:2f}")
        print("===========================================")

    elif Opcao == "0":
        break

    else:
        print("operação inválida por favor selecione novamente a opção desejada.")