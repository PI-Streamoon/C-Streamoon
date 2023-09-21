import mysql.connector
import monitoring_server as ms


loginAttempts = 5
def connectionDatabase():
  userDatabase = str(input("-> Informe o seu usuário do banco: "))
  passDatabase = str(input("-> Informe a sua senha do banco: "))

  try:
    connection = mysql.connector.connect(
        host = 'localhost',
        user = userDatabase,
        password = passDatabase,
        database = 'streamoon',
    )
    print("Connected database")
    # ms.captureServerData(connection)
    # ms.checkServerExists(connection)
    connection.close()
  
  except Exception as e:
    global loginAttempts
    if loginAttempts > 1: 
      loginAttempts -= 1
      print(f"Usuário ou senha digitado incorretamente!")
      print(f"Tentavivas: {loginAttempts}")
      print(f"This is error: {e}\n")
      connectionDatabase()
    else:
      connection.close()
      print('Seu chefe foi alertado')


def validateCompanyLogin():
  connection = mysql.connector.connect(
        host = 'localhost',
        user = 'root',
        password = '@eduufreire',
        database = 'streamoon',
    )
  cursor = connection.cursor()

  codLogin = str(input('Informe o CÓDIGO de login(Empresa):'))
  passLogin = str(input('Informe a SENHA de login(Empresa):'))

  if codLogin != "" and passLogin != "":
    sqlQuery = (f"select idEmpresa from empresa where codLogin = {codLogin} and passLogin = {passLogin};")
    cursor.execute(sqlQuery)
    print(cursor.fetchone())
    

validateCompanyLogin()
# connectionDatabase()
