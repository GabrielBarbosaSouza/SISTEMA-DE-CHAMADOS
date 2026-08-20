from rich import print
from time import sleep
from rich.traceback import install
from InquirerPy import inquirer
from banco.conexao import db, cursor
from funcoes.chamados import abrir_chamados, detalhes_chamado, meus_chamados
from funcoes.usuarios import cadastrar_usuario
from funcoes.dashboard import dashboard
from menus.menu_chamados import menu_chamados

install()
    

def sair():
    print("[red]Encerrando sistema", end='')

    for _ in range(3):
        sleep(1)
        print("[red].[/]", end='')

    print("\nVolte sempre!")

    cursor.close()
    db.close()


def menu_ti():
    while True:
        print("\n[blue]=== SISTEMA DE CHAMADOS ===[/]")

        opcao = inquirer.select(
            message='Escolha uma das opções:',
            choices=[
                "1 - Abrir chamado",
                "2 - Meus chamados",
                "3 - Ver detalhes do chamado",
                "4 - Gerenciar chamados - TI",
                "5 - Cadastrar usuário - TI",
                "6 - Dashboard - TI",
                "7 - Sair"
            ]
        ).execute()

        match opcao:
            case "1 - Abrir chamado":
                abrir_chamados()

            case "2 - Meus chamados":
                meus_chamados()

            case "3 - Ver detalhes do chamado":
                detalhes_chamado()

            case "4 - Gerenciar chamados - TI":
                menu_chamados()

            case "5 - Cadastrar usuário - TI":
                cadastrar_usuario()

            case "6 - Dashboard - TI":
                dashboard()

            case "7 - Sair":
                sair()
                break