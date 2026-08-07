from InquirerPy import inquirer

opcao = inquirer.select(
    message = "Escolha uma opção",
    choices = [1,
               2,
               3,
               4]
)

opcao.execute()