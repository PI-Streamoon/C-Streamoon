import mysql.connector
import bcrypt

connection = mysql.connector.connect(
        host='localhost',
        database='streamoon',
        user='StreamoonUser',
        password='Moon2023'
    )

cursor = connection.cursor()

print('+='*15, 'Login', '+='*15)

while True:
    email = input("Digite o seu Email: ")
    senha = input("Digite a senha: ")

    cursor.execute(f"SELECT * FROM usuario WHERE email = '{email}'")

    user_by_email = cursor.fetchone()


    if user_by_email != None and bcrypt.checkpw(senha.encode('utf-8'), user_by_email[4].encode('utf-8')):
        break
    else:
        print("")
        print("Email ou Senha Incorretos. Tente Novamente")
        print("")