from banco.conexao import cursor
from rich import print

def login():
    while True:
        matricula = input("Digite sua matrícula (4 primeiros dígitos do CPF): ").strip()

        if not (len(matricula) == 4 and matricula.isdigit()):
            print("[yellow]Digite exatamente 4 números.[/]")
            continue
        
        cursor.execute("""
            SELECT nome, matricula, perfil
            FROM usuarios
            WHERE matricula = %s
        """, (matricula,))

        usuario = cursor.fetchone()

        if usuario:
            return usuario

        print("[red]Usuário não encontrado.[/]")
