from rich import print
from modelos.usuario import Usuario
from banco.conexao import db, cursor

def cadastrar_usuario():
    while True:
        nome = input("Digite o nome do cadastrado: ").strip()
        
        if nome:
            break
        print("[yellow]O nome não pode ficar vazio.[/]")

    while True:
        email = input("Digite o e-mail do cadastrado: ").strip().lower()
        
        cursor.execute("""
            SELECT id FROM usuarios
            WHERE email = %s
        """, (email,))

        if cursor.fetchone():
            print("[yellow]Já existe um usuário com esse e-mail.[/]")
            continue
        break

    while True:
        matricula = input(" Digite o ID do cadastrado (4 primeiros dígitos do CPF): ").strip()

        if not (len(matricula) == 4 and matricula.isdigit()):
            print("[yellow]Digite exatamente 4 números.[/]")
            continue

        cursor.execute("""
            SELECT id FROM usuarios
            WHERE matricula = %s
        """, (matricula,))

        if cursor.fetchone():
            print("[yellow]Já existe um usuário com essa matrícula.[/]")
            continue
        break

    usuario = Usuario(
        nome=nome,
        email=email,
        matricula=matricula
    )

    cursor.execute("""
        INSERT INTO usuarios (nome, email, matricula)
        VALUES (%s, %s, %s)
    """, (
        usuario.nome,
        usuario.email,
        usuario.matricula
    ))

    db.commit()

    print("\n[green]Usuário cadastrado com sucesso![/]")