from rich.traceback import install
from funcoes.login import login
from menus.menu_ti import menu_ti
from menus.menu_user import menu_user
from rich import print

install()


def main():
    nome, matricula, perfil = login()

    print(f"\n[green]Bem-vindo, {nome}![/]")

    if perfil == "TI":
        menu_ti()
    else:
        menu_user()

if __name__ == '__main__':
    main()