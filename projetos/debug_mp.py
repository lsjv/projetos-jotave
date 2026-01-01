import time
import sys
import winsound

def escrever(texto, delay=0.02):
    for char in texto:
        sys.stdout.write(char)
        sys.stdout.flush()

        if char != " ":
            winsound.Beep(800, 30)  # frequência, duração

        time.sleep(delay)
    print()

def caixa_dialogo(texto):
    largura = len(texto) + 4

    print("┌" + "─" * largura + "┐")
    print("│  ", end="")
    escrever(texto)
    print("└" + "─" * largura + "┘")

def escolha(opcoes):
    print("\nO que voce vai fazer?\n")

    for i, opcao in enumerate(opcoes, 1):
        print(f" {i}. {opcao}")

    while True:
        escolha = input("\n> ")
        if escolha.isdigit() and 1 <= int(escolha) <= len(opcoes):
            return int(escolha)
        else:
            print("Escolha invalida, humano.")



caixa_dialogo("Ei, humano...")
caixa_dialogo("Voce realmente acha que pode escapar?")

opcao = escolha(["Lutar", "Conversar", "Fugir"])

if opcao == 1:
    caixa_dialogo("Voce escolheu violencia.")
    caixa_dialogo("Voce ataca com a espada, mas ela quebra")
elif opcao == 2:
    caixa_dialogo("Voce tenta conversar...")
elif opcao == 3:
    caixa_dialogo("Voce corre como um covarde.")
