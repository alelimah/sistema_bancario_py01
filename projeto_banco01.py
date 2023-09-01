from os import system
from datetime import date
import re
import textwrap

system("clear")
saudacao = "=============== Seja Bem Vindo! ================"

menu = """\n==== Escolha uma das opções para continuar. ====
[e] - Extrato 
[s] - Saque
[d] - Depósito
[nu] - Cadastrar Usuário
[lu] - Listar Usuários
[nc] - Criar Conta
[lc] - Listar Contas
[f] - Finalizar

=> """

print(saudacao)

def criar_usuario(usuarios):
    while True:
        cpf = input("Informe o CPF (apenas os números): ")
        cpf_valido = len(cpf) == 11

        # Verificar se usuário já está cadastrado
        if cpf_valido:
            cpf_cadastrado = filtrar_usuario(usuarios,cpf)
            pass
        else:
            print("Insira um CPF com 11 dígitos!")
            continue
            
        if cpf_cadastrado:
            print("====== CPF já cadastrado! ======")
            return
        break

    nome = input("Informe o nome completo: ")
    
    # Cadastrar data de nascimento
    while True:
        # DIA
        dia_nascimento = input("Informe o dia de nascimento (dd): ")
        dia_match = re.fullmatch("[0-9][0-9]",dia_nascimento)
        if dia_match:
            pass
        else:
            print("Não deu match")
            continue
        # MÊS
        mes_nascimento = input("Informe o mês de nascimento (mm): ")
        mes_match = re.fullmatch("[0-9][0-9]",mes_nascimento)
        if mes_match:
            pass
        else:
            print("Não deu match")
            continue
        # ANO
        ano_nascimento = input("Informe o ano de nascimento (aaaa): ")
        ano_match = re.fullmatch("[0-9][0-9][0-9][0-9]",ano_nascimento)
        if ano_match:
            nascimento = (dia_nascimento, mes_nascimento, ano_nascimento)
            data_nascimento = "/".join(nascimento)
            break
        else:
            print("Não deu match")
            continue
        
    # Cadastrar endereço
    logradouro = input("Informe o logradouro: ")
    numero_casa = input("Informe o número: ")
    bairro = input("Informe o bairro: ")
    cidade = input("Informe a cidade: ")
    estado = input("Informe UF: ")
    endereco = (logradouro + ', ' + numero_casa + ' - ' + bairro + ' - ' + cidade + '/' + estado.upper())
    
    
    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("===== USUÁRIO CRIADO COM SUCESSO =====")
    print(usuarios[-1])
        
def listar_usuarios(usuarios):
    for usuario in usuarios:
        print(usuario)

def filtrar_usuario(usuarios,cpf):
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None

def criar_conta(agencia, numero_conta, usuarios):
    cpf = input("Informe o CPF do usuário: ")
    usuario = filtrar_usuario(usuarios, cpf)
    
    if usuario:
        print("======= Conta criada com sucesso! =======")
        return {"usuario": usuario, "agencia": agencia, "numero_conta": numero_conta}
    else:
        print("======= Usuário não identificado =======")
    
def listar_contas(contas):
    for conta in contas:
        conta_formatada = f'''\
            Agência:\t{conta["agencia"]}
            C/C:\t\t{conta["numero_conta"]}
            Titular:\t{conta["usuario"]["nome"]}
        '''
        print("=" * 50)
        print(textwrap.dedent(conta_formatada))

def sacar(*, valor, saldo, extrato, data, limite):
    
    valor_numerico = type(valor) != float
    saldo_inferior = valor > saldo
    limite_excedido = valor > 500
    saques_excedidos = limite <= 0
        
    if valor_numerico:
        print("Insira um valor válido.")
    elif valor < 0:
        system("clear")
        print("Insira um valor maior que R$0.00 para depositar.")
    elif saldo_inferior:
        system("clear")
        print(f"Insira um valor inferior a {saldo:.2f}.")
    elif limite_excedido:
        system("clear")
        print("Insira um valor inferior a R$500.00.")
    elif saques_excedidos:
        system("clear")
        print("Excedeu seu limite de saques diários.")
    else:
        system("clear")
        saldo -= valor
        print(
            f"SAQUE REALIZADO COM SUCESSO!\n"
            f"\nO saque foi de R${valor:.2f}.\n"
            f"O novo saldo é R${saldo:.2f}."
        )
        extrato.append(f"{data:%d/%m/%Y}\t\t\t{valor:>10.2f} -")
        limite -= 1
        print(f"\nSaques que ainda pode realizar hoje: {limite}.")
        
    return saldo, extrato, limite

def depositar(valor, saldo, extrato, data, /):
    if valor > 0:
        system("clear")
        saldo += valor
        print(
            f"DEPÓSITO REALIZADO COM SUCESSO!\n"
            f"\nO depósito foi de R${valor:.2f}.\n"
            f"O novo saldo é R${saldo:.2f}."
        )
        extrato.append(f"{data:%d/%m/%Y}\t\t\t{valor:>10.2f} +")
    else:
        system("clear")
        print("Insira um valor maior que R$0.00 para depositar.")
        
    return saldo, extrato
    
def imprime_extrato(saldo, /, *, extrato):
    print("================== EXTRATO ==================")
    print(
        "Não existem movimentações a serem exibidas!"
    ) if not extrato else gerar_extrato(extrato)
    print(f"\nSALDO: R${saldo:.2f}.")
    print("=============================================")
        
def gerar_extrato(extrato):
    for operacao in extrato:
        print(operacao)


def main():
    extrato = []
    usuarios = []
    contas = []
    AGENCIA = "0001"
    numero_conta = 1
    saldo = 500.0
    limite_diario = 3

    while True:
        d = date.today()
        opcao = input(menu).lower()
        system("clear")

        # EXTRATO
        if opcao == "e":
            imprime_extrato(saldo, extrato=extrato)

        # SAQUE
        elif opcao == "s":
            print(f"Seu saldo atual é: R${saldo:.2f}.")
            valor = float(input("Qual o valor que deseja sacar?\n"))
            saldo, extrato, limite_diario = sacar(valor=valor, saldo=saldo, extrato=extrato, data=d, limite=limite_diario)

        # DEPÓSITO
        elif opcao == "d":
            print(f"Seu saldo atual é: R${saldo:.2f}.")
            valor = float(input("Qual o valor que deseja depositar?\n"))
            saldo, extrato = depositar(valor, saldo, extrato, d)

        # CADASTRAR USUÁRIO
        elif opcao == "nu":
            criar_usuario(usuarios)
        
        # LISTAR USUÁRIOS
        elif opcao == "lu":
            listar_usuarios(usuarios)

        # CRIAR CONTA
        elif opcao == "nc":
            conta = criar_conta(AGENCIA, numero_conta, usuarios)

            if conta:
                contas.append(conta)
                numero_conta += 1


        # LISTAR CONTAS
        elif opcao == "lc":
            listar_contas(contas)

        # FINALIZAR
        elif opcao == "f":
            system("clear")
            print("===========================\nObrigado. Até a próxima!\n")
            break

        else:
            print("Insira uma opção válida.")

main()
