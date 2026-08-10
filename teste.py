import mysql.connector
from rich import print
from rich.table import Table
from rich.traceback import install
from time import sleep
from InquirerPy import inquirer
from modelos.usuario import Usuario
from modelos.chamado import Chamado

install()

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Gabriel1!",
        database="script"
    )
    
except mysql.connector.Error as erro:
    print(f"[red]ERRO!: {erro}")
    exit()

cursor = db.cursor()

def cadastrar_usuario():
    while True:
        nome = input("Digite o seu nome: ").strip()
        
        if nome:
            break
        print("[yellow]O nome não pode ficar vazio.[/]")

    while True:
        email = input("Digite o seu e-mail: ").strip().lower()
        
        cursor.execute("""
            SELECT id FROM usuarios
            WHERE email = %s
        """, (email,))

        if cursor.fetchone():
            print("[yellow]Já existe um usuário com esse e-mail.[/]")
            continue
        break

    while True:
        matricula = input("Seu ID (4 primeiros dígitos do CPF): ").strip()

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

    
def abrir_chamados():
    while True:
        titulo = input("Título: ").strip()

        if titulo:
            break
        print("[yellow]O Título não pode ficar vázio![/]")


    while True:
        descricao = input("Descrição: ").strip()

        if descricao:
            break
        print("[yellow]A Descricao não pode ficar vázia![/]")


    while True:
        categoria = input("Categoria: ").strip()

        if categoria:
            break
        print("[yellow]A Categoria não pode ficar vázia![/]")


    while True:
        prioridade = input("Prioridade ([Baixa/Media/Alta]): ").lower()

        if prioridade in ["baixa", "media", "alta"]:
            break
        print("[red]Prioridade inválida.[/]")
    
    
    while True:
        matricula = input("Seu ID (4 primeiros dígitos do CPF): ")

        if len(matricula) == 4 and matricula.isdigit():
            break
        print("[red]Digite exatamente 4 números.[/]")
    
    
    cursor.execute("SELECT id FROM usuarios WHERE matricula = %s", (matricula,))

    resultado = cursor.fetchone()
    if resultado is None:
        print("[red]Usuário não encontrado.[/]")
        return
    
    id_usuario = resultado[0]

    chamado = Chamado(
        titulo = titulo,
        descricao = descricao,
        categoria = categoria,
        prioridade = prioridade,
        id_usuario = id_usuario
    )
    
    cursor.execute("""
        INSERT INTO chamados
        (titulo, descricao, categoria, prioridade, id_usuario)
        VALUES (%s, %s, %s, %s, %s)
    """, (chamado.titulo, chamado.descricao, chamado.categoria, chamado.prioridade, chamado.id_usuario))

    db.commit()
    print("\n[green]Chamado aberto![/]")


def listar_chamados():    
    cursor.execute("""
        SELECT id, titulo, categoria, prioridade, status
        FROM chamados
        ORDER BY id DESC
    """)
    
    chamados = cursor.fetchall()
    if not chamados:
        print("\n[red]Nenhum chamado encontrado.[/]")
        return
    
    tabela_chamados = Table()
    tabela_chamados.add_column("ID")
    tabela_chamados.add_column("Título")
    tabela_chamados.add_column("Categoria")
    tabela_chamados.add_column("Prioridade")
    tabela_chamados.add_column("Status")
    
    for id_chamado, titulo, categoria, prioridade, status in chamados:
        tabela_chamados.add_row(str(id_chamado), str(titulo), str(categoria), str(prioridade), str(status))

    print(tabela_chamados)


# def meus_chamados():
    


def detalhes_chamado():
    while True:
        try:
            id_chamado = int(input("ID do Chamado: "))
            break
        except ValueError:
            print("[yellow]Digite apenas números.[/]")
    
    cursor.execute("""
        SELECT
        c.id AS id_chamado,
        u.nome AS nome_usuario,
        u.matricula,
        c.titulo,
        c.descricao,
        c.categoria,
        c.prioridade,
        c.status,
        c.data_abertura,
        c.data_fechamento
        FROM chamados c
        JOIN usuarios u
            ON c.id_usuario = u.id
        WHERE c.id = %s;
        """, (id_chamado,))

    chamados = cursor.fetchone()
    if not chamados:
        print("[red]Nenhum chamado encontrado.[/]")
        return
    
    tabela_chamados = Table()
    tabela_chamados.add_column("ID")
    tabela_chamados.add_column("Nome")
    tabela_chamados.add_column("Matricula")
    tabela_chamados.add_column("Título")
    tabela_chamados.add_column("Descrição")
    tabela_chamados.add_column("Categoria")
    tabela_chamados.add_column("Prioridade")
    tabela_chamados.add_column("Status")
    tabela_chamados.add_column("Data Abertura")
    tabela_chamados.add_column("Data Fechamento")
    
    tabela_chamados.add_row(
        str(chamados[0]),
        str(chamados[1]),
        str(chamados[2]),
        str(chamados[3]),
        str(chamados[4]),
        str(chamados[5]),
        str(chamados[6]),
        str(chamados[7]),
        str(chamados[8]),
        str(chamados[9])
    )

    print(tabela_chamados)
     
    
def fechar_chamados():
    listar_chamados()

    while True:
        try:
            id_chamado = int(input("\nID do chamado que deseja fechar: "))
            break
        except ValueError:
            print("[yellow]Digite apenas números.[/]")
    
    cursor.execute("""
        SELECT status FROM chamados
        WHERE id = %s
    """,(id_chamado,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("[red]Chamado não encontrado.[/]")
        return

    cursor.execute("""
        UPDATE chamados
        SET status = 'Fechado'
        WHERE id = %s
        AND status != 'Fechado'
    """, (id_chamado,))

    if cursor.rowcount > 0:
        db.commit()
        print("\n[green]Chamado fechado![/]")
    else:
        print("\n[yellow]Esse chamado já está fechado.[/]")


def sair():
    print("[red]Encerrando sistema", end='')

    for _ in range(3):
        sleep(1)
        print("[red].[/]", end='')

    print("\nVolte sempre!")

    cursor.close()
    db.close()


def main():   
    while True:
        print("\n[blue]=== SISTEMA DE CHAMADOS ===[/]")
        opcao = inquirer.select(
            message = 'Escolha uma das opções:',
            choices = [
                "1 - Abrir chamado",
                "2 - Listar chamado",
                "3 - Ver detalhes do chamado",
                "4 - Fechar chamado",
                "5 - Cadastrar usuario",
                "6 - Sair"
            ]
        ).execute()

        if opcao == "1 - Abrir chamado":
            abrir_chamados()
        elif opcao == "2 - Listar chamado":
            listar_chamados()
        elif opcao == "3 - Ver detalhes do chamado":
            detalhes_chamado()
        elif opcao == "4 - Fechar chamado":
            fechar_chamados()
        elif opcao == "5 - Cadastrar usuario":
            cadastrar_usuario()
        elif opcao == "6 - Sair":
            sair()
            break
        else:
            print("Opção inválida.")
    
if __name__ == '__main__':
    main()