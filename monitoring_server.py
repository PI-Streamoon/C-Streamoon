import mysql.connector
import datetime
from datetime import date
import time
import psutil
import platform
# import random



def checkServerExists(connection):
    cursor = connection.cursor()

    try:
        networkName = platform.node()
        # if networkName == "":
        #     networkName = "nameServer-not-found"
        # else:
        #     protocolRand = random.randint(1, 5000)
        #     networkName += (f"&{round(protocolRand, 4)}")
        sqlQuery = (f"select * from servidor where nomeServidor like '%{networkName}%'")
        cursor.execute(sqlQuery)

        if cursor.fetchone() == "":
            print('Existe')
        else:
            print('Não existe')

    except Exception as e:
        print(f"This is error: {e}")
        
  


def captureServerData(connec):

    connection = mysql.connector.connect(
        host = "localhost",
        user = connec.user,
        password = connec._password,
        database = connec.database
    )

    print("[+]" + "=" * 170 + "[+]")
    print(
        """\u001b[35m
    #    ______     __                                                   ______                                                    
    #   /      \   |  \                                                 /      \                                                  
    #  |  $$$$$$\ _| $$_     ______    ______    ______   ______ ____  |  $$$$$$\  ______    _______  __    __   ______    ______  
    #  | $$___\$$|   $$ \   /      \  /      \  |      \ |      \    \ | $$___\$$ /      \  /       \|  \  |  \ /      \  /      \\
    #   \$$    \  \$$$$$$  |  $$$$$$\|  $$$$$$\  \$$$$$$\| $$$$$$\$$$$\ \$$    \ |  $$$$$$\|  $$$$$$$| $$  | $$|  $$$$$$\|  $$$$$$
    #   _\$$$$$$\  | $$ __ | $$   \$$| $$    $$ /      $$| $$ | $$ | $$ _\$$$$$$\| $$    $$| $$      | $$  | $$| $$   \$$| $$    $$
    #  |  \__| $$  | $$|  \| $$      | $$$$$$$$|  $$$$$$$| $$ | $$ | $$|  \__| $$| $$$$$$$$| $$_____ | $$__/ $$| $$      | $$$$$$$$
    #   \$$    $$   \$$  $$| $$       \$$     \ \$$    $$| $$ | $$ | $$ \$$    $$ \$$     \ \$$     \ \$$    $$| $$       \$$    
    #    \$$$$$$     \$$$$  \$$        \$$$$$$$  \$$$$$$$ \$$  \$$  \$$  \$$$$$$   \$$$$$$$  \$$$$$$$  \$$$$$$  \$$        \$$$$$$$
    #  
    #                                                   Developed by Streamoon\u001b[0m
    """
    )
    print("[+]" + "=" * 170 + "[+]\n")


    print(f"Network Name: {platform.node()}")
    print(f"Processor: {platform.processor()}")
    print(f"Operating System: {platform.system()}")


    # Construindo o cabeçalho que indica o tipo de dado que cada coluna exibe
    headerConsole = "   Date      |      Hour      |"
    cpuQuantity = psutil.cpu_count(logical=True)
    for i in range(cpuQuantity):
        headerConsole += "      "
        headerConsole += f"\u001b[34;1mCPU{i+1}\u001b[0m" + "      |"
    headerConsole += "    \u001b[35;1mMemory (%)\u001b[0m   |  Memory Used(GB)  |  Memory Total(GB)  |      Diks"
    print("\n[+]" + "=" * 170 + "[+]\n")
    print(headerConsole + "\n")


    # Capturar os dados de CPU/RAM/DISK a cada 2segs
    while True:

        cpusPercent = psutil.cpu_percent(interval=1, percpu=True)  
        memory = (psutil.virtual_memory())                         
        percentualMemoria = memory.percent

        memoryUsed = ((memory.used / 1024) / 1024) / 1000          
        memoryTotal = ((memory.total / 1024) / 1024) / 1000        
        diskPercent = psutil.disk_usage("/")                      


        mensagem = time.strftime(f"   %d/%m/%Y   |   %H:%M   |", time.localtime())

        somaCpus = 0
        mediaCpus = 0
        for i in range(len(cpusPercent)):
            somaCpus += cpusPercent[i]
            mensagem += ("      " + f"\u001b[34;1m{cpusPercent[i]}%\u001b[0m" + "      |")  # Percentuais das CPUs
        mediaCpus = somaCpus / len(cpusPercent)

        # Construindo a mensagem que vai ser exibida no console
        mensagem += ("       " + f"\u001b[35;1m{memory.percent}%\u001b[0m" + "       |")  # Percentual da Memoria
        mensagem += ("       " + f"{round(memoryUsed, 1)}" + "       |")                  # Qtde de memória usada
        mensagem += ("       " + f"{round(memoryTotal, 1)}" + "       |")                 # Qtde total da memória
        mensagem += ("       " + f"{diskPercent.percent}%")                               # Percentual do Disco

        # print(mensagem)

        agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
                       
                        
                        print(connection)
                      
                        mySql_insert_query_cpu_percent = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(mediaCpus) + ", '" + str(agora) + "', 1);"
                        mySql_insert_query_memory = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(percentualMemoria) + ", '" + str(agora) + "', 2);"
                        mySql_insert_query_memory_used = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(memoryUsed) + ", '" + str(agora) + "', 3);"
                        mySql_insert_query_memory_total = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(memoryTotal) + ", '" + str(agora) + "', 4);"
                        mySql_insert_query_disc_percent = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(diskPercent.percent) + ", '" + str(agora) + "', 5);"

                        cursor = connection.cursor()
                        cursor.execute(mySql_insert_query_cpu_percent)
                        cursor.execute(mySql_insert_query_memory)
                        cursor.execute(mySql_insert_query_memory_used)
                        cursor.execute(mySql_insert_query_memory_total)
                        cursor.execute(mySql_insert_query_disc_percent)
                        
                        connection.commit()
                        time.sleep(5)
                        # print(cursor.rowcount, "Record inserted successfully into Laptop table")
                        cursor.close()


        except mysql.connector.Error as error:
                        print("Failed to insert record into Laptop table {}".format(error))

        finally:
                        if connection.is_connected():
                            # connection.close()
                            print("MySQL connection is closed")

        time.sleep(2)