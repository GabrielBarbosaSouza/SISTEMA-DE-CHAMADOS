import mysql.connector

try:
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="??????",
        database="script"
    )
    
except mysql.connector.Error as erro:
    print(f"[red]ERRO!: {erro}")
    exit()

cursor = db.cursor()
