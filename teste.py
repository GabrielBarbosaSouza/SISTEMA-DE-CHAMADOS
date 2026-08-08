import mysql.connector
from rich import print
from time import sleep
from InquirerPy import inquirer

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

def abrir_chamados():
    titulo = input("Título: ")
    descricao = input("Descrição: ")
    categoria = input("Categoria: ")
    while True:
        prioridade = input("Prioridade ([Baixa/Media/Alta]): ").lower()

        if prioridade in ["baixa", "media", "alta"]:
            break
        print("Prioridade inválida.")
    
    
    while True:
        matricula = input("Seu ID (4 primeiros dígitos do CPF): ")

        if len(matricula) == 4 and matricula.isdigit():
            break
        print("Digite exatamente 4 números.")

    cursor.execute("SELECT id FROM usuarios WHERE matricula = %s", (matricula,))

    resultado = cursor.fetchone()
    if resultado is None:
        print("Usuário não encontrado.")
        return
    
    id_usuario = resultado[0]

    cursor.execute("""
        INSERT INTO chamados
        (titulo, descricao, categoria, prioridade, id_usuario)
        VALUES (%s, %s, %s, %s, %s)
    """, (titulo, descricao, categoria, prioridade, id_usuario))

    db.commit()
    print("\n[green]Chamado aberto![/]")

def listar_chamados():
    print()
    cursor.execute("""
        SELECT id, titulo, categoria, prioridade, status
        FROM chamados
    """)
    
    chamados = cursor.fetchall()
    if not chamados:
        print("\n[red]Nenhum chamado encontrado.[/]")
        return
    
    for id_chamado, titulo, categoria, prioridade, status in chamados:
        print(
            f"ID: {id_chamado} | "
            f"Título: {titulo} | "
            f"Categoria: {categoria} | "
            f"Prioridade: {prioridade} | "
            f"Status: {status}"
        )

def fechar_chamados():
    listar_chamados()

    while True:
        try:
            id_chamado = int(input("\nID do chamado que deseja fechar: "))
            break
        except ValueError:
            print("Digite apenas números.")
    
    cursor.execute(
    "SELECT status FROM chamados WHERE id = %s",(id_chamado,))

    resultado = cursor.fetchone()

    if resultado is None:
        print("Chamado não encontrado.")
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


def main():   
    while True:
        print("\n[blue]=== SISTEMA DE CHAMADOS ===[/]")
        opcao = inquirer.select(
            message = 'Escolha uma das opções:',
            choices = ["1 - Abrir chamado",
                       "2 - Listar chamado",
                       "3 - Fechar chamado",
                       "4 - Sair"]).execute()

        if opcao == "1 - Abrir chamado":
            abrir_chamados()
        elif opcao == "2 - Listar chamado":
            listar_chamados()
        elif opcao == "3 - Fechar chamado":
            fechar_chamados()
        elif opcao == "4 - Sair":
            print("[red]Encerrando sistema", end='')
            
            for _ in range(3):
                sleep(1)
                print("[red].[/]", end='')
            
            print("Volte sempre!")
    
            cursor.close()
            db.close()
            break
        else:
            print("Opção inválida.")
    
if __name__ == '__main__':
    main()