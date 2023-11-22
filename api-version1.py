import mysql.connector
import datetime
from datetime import date
import time
import psutil
import platform
import os
import pandas as pd
import connectionJira
import login
from sklearn.linear_model import LinearRegression

consoleColors = {
    "black": "\u001b[30m",
    "red": "\u001b[31m",
    "green": "\u001b[32m",
    "yellow": "\u001b[33m",
    "blue": "\u001b[34m",
    "magenta": "\u001b[35m",
    "cyan": "\u001b[36m",
    "white": "\u001b[37m",
    "brightBlack": "\u001b[30;1m",
    "brightRed": "\u001b[31;1m",
    "brightGreen": "\u001b[32;1m",
    "brightYellow": "\u001b[33;1m",
    "brightBlue": "\u001b[34;1m",
    "brightMagenta": "\u001b[35;1m",
    "brightCyan": "\u001b[36;1m",
    "brightWhite": "\u001b[37;1m",
    "reset": "\u001b[0m",
}

def sendSlack(msg):
    mensagemSlack = {
        "blocks": [
            {
                "type": "section",
                "text": {
                    "type": "plain_text",
                    "emoji": True,
                    "text": "🚨 Algum componente de seu servidor está com o uso acima do normal"
                }
            },
            {
                "type": "divider"
            },
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": "\n{}\nBuilding 2 - Havarti Cheese (3)\n2 guests".format( datetime.datetime.now().strftime("%A, %B %d %H:%M:%S") )
                },
                "accessory": {
                    "type": "image",
                    "image_url": "https://cdn.icon-icons.com/icons2/1852/PNG/512/iconfinder-serverrack-4417101_116637.png",
                    "alt_text": "calendar thumbnail"
                }
            },
            {
                "type": "context",
                "elements": [
                    {
                        "type": "image",
                        "image_url": "https://api.slack.com/img/blocks/bkb_template_images/notificationsWarningIcon.png",
                        "alt_text": "notifications warning icon"
                    },
                    {
                        "type": "mrkdwn",
                        "text": f"*{msg}*"
                    }
                ]
            },
            {
                "type": "divider"
            }
        ]
    }

    suporte = "https://hooks.slack.com/services/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"
    #postMsg = requests.post(suporte, data=json.dumps(mensagemSlack))

def writeDB(registro: float, dataHora: datetime.datetime, fkComponenteServidor: int):
    mySql_insert = f"INSERT INTO registro (registro, dtHora, fkComponenteServidor) VALUES ({registro}, '{dataHora}', {fkComponenteServidor});"

    cursor = connection.cursor()
    cursor.execute(mySql_insert)

    connection.commit()
    cursor.close()

def showText():
    print(f"""{consoleColors['magenta']}
        []====================================================================================[]
        |                                                                                      |      
        |   ███████╗████████╗██████╗ ███████╗ █████╗ ███╗   ███╗ ██████╗  ██████╗ ███╗   ██╗   |
        |   ██╔════╝╚══██╔══╝██╔══██╗██╔════╝██╔══██╗████╗ ████║██╔═══██╗██╔═══██╗████╗  ██║   |
        |   ███████╗   ██║   ██████╔╝█████╗  ███████║██╔████╔██║██║   ██║██║   ██║██╔██╗ ██║   |
        |   ╚════██║   ██║   ██╔══██╗██╔══╝  ██╔══██║██║╚██╔╝██║██║   ██║██║   ██║██║╚██╗██║   |
        |   ███████║   ██║   ██║  ██║███████╗██║  ██║██║ ╚═╝ ██║╚██████╔╝╚██████╔╝██║ ╚████║   |
        |   ╚══════╝   ╚═╝   ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚═╝     ╚═╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═══╝   |
        |                                                                                      |
        |                               Developed by Streamoon                                 |
        []====================================================================================[]{consoleColors['reset']}""")

    print(f"""{consoleColors['magenta']}
            Network Name: {platform.node()}
            Processor: {platform.processor()}
            Operating System: {platform.system()}\n
        []====================================================================================[]{consoleColors['reset']}""")


indexHour = []
consoleData = {
    "CPU": [],
    "Frequência CPU":[],
    "MemoryPercent" : [],
    "MemoryUsed" : [],
    "MemoryTotal" : [],
    "Disk" : [],
    "DiskInput" : [],
    "DiskOutput" : [],
    "Upload": [],
    "Download": []
}
cpuQuantity = psutil.cpu_count(logical=True)
for i in range(cpuQuantity):
    cpuName = (f"CPU{i+1}")
    consoleData[cpuName] = []

arrayCPU = []
arrayRAM = []
arrayUpload = []
arrayDownload = []


# Capturar os dados de CPU/RAM/DISK/UPLOAD/DOWNLOAD a cada 2segs
while True:

    cpusPercent = psutil.cpu_percent(interval=1, percpu=True)

    memory = (psutil.virtual_memory())
    memPercent = memory.percent
    memoryUsed = round((memory.used / 1024 / 1024 / 1000), 1)   
    memoryTotal = round((memory.total / 1024 / 1024 / 1000), 1)
    upload = round((psutil.net_io_counters().bytes_sent / 1e6), 1)
    download = round((psutil.net_io_counters().bytes_recv / 1e6), 1)

    diskPartitions = psutil.disk_partitions()
    diskPercent = psutil.disk_usage(diskPartitions[0].mountpoint)                      
    diskInput = round((psutil.disk_io_counters().read_bytes / 1e9), 2)
    diskOutput = round((psutil.disk_io_counters().write_bytes / 1e9), 2)

    somaCpus = 0
    mediaCpus = 0
    for i in range(psutil.cpu_count()):
        somaCpus += cpusPercent[i]
        cpuName1 = (f"CPU{i+1}") 
        consoleData[cpuName1].append(cpusPercent[i])
    mediaCpus = int(round((somaCpus / len(cpusPercent)),0))
    frequenciaCpu = int(round(psutil.cpu_freq().current,0))


    dateNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    indexHour.append(dateNow)

    systemClear = ('clear' if platform.system() == 'Linux' else 'cls')
    os.system(systemClear)

    showText()
    consoleData["CPU"].append(mediaCpus)
    consoleData["Frequência CPU"].append(frequenciaCpu)
    consoleData["MemoryPercent"].append(memPercent)
    consoleData["MemoryUsed"].append(memoryUsed)
    consoleData["MemoryTotal"].append(memoryTotal)
    consoleData["Disk"].append(diskPercent.percent)
    consoleData["DiskInput"].append(diskInput)
    consoleData["DiskOutput"].append(diskOutput)
    consoleData["Upload"].append(upload)
    consoleData["Download"].append(download)
    
    #Integração slack!
    mensagemSlack = ""
    if (memPercent > 80):
        #connectionJira.chamado("Crítico", "A MEMORIA VIRTUAL ESTÁ ACIMA DE 80%")

        sendSlack("A MEMORIA VIRTUAL ESTÁ ACIMA DE 80%")
    
       
        
    for i in range(len(cpusPercent)):
        if int(cpusPercent[i])> 90:
            #connectionJira.chamado("Crítico", "O CPU VIRTUAL ESTÁ ACIMA DE 90%")
            sendSlack(f"O CPU VIRTUAL {i} ESTÁ ACIMA DE 90%")
           
    if (mediaCpus> 90):
        #connectionJira.chamado("Crítico", "A SUA MÉDIA DE CPU ULTRAPASSOU 90%")
        sendSlack("A SUA MÉDIA DE CPU ULTRAPASSOU 90%")

        
    if (download < 100):
        #connectionJira.chamado("Crítico", "A SUA ENTRADA DE REDE (DOWNLOAD) ESTÁ ABAIXO DE 100Mb")
        sendSlack("A SUA ENTRADA DE REDE (DOWNLOAD) ESTÁ ABAIXO DE 100Mb")

        
    if (upload < 40):
        #connectionJira.chamado("Crítico", "A SUA SAÍDA DE REDE (UPLOAD) ESTÁ ABAIXO DE 40Mb")
        sendSlack("A SUA SAÍDA DE REDE (UPLOAD) ESTÁ ABAIXO DE 40Mb")
        
    
    df = pd.DataFrame(data=consoleData, index=indexHour)
    print(f"\n{df}")


    connection = mysql.connector.connect(
        host='localhost',
        database='streamoon',
        user='StreamoonUser',
        password='Moon2023'
    )

    count = 0
    arrayCPU.append(mediaCpus)
    arrayRAM.append(memoryUsed)
    arrayUpload.append(upload)
    arrayDownload.append(download)

    count += 1

    if len(arrayCPU) >= 10 and len(arrayRAM) >= 10 and len(arrayUpload) >= 10 and len(arrayDownload) >= 10:
  
        cpuPredict = ([arrayCPU])
        ramPredict = ([arrayRAM])
        uploadPredict = ([arrayUpload])
        downloadPredict = ([arrayDownload])
        
        model1 = LinearRegression()
        model1.fit(ramPredict, cpuPredict) # troquei a ordem awui

        model2 = LinearRegression()
        model2.fit(downloadPredict, uploadPredict)

        predictionCPU = model1.predict(cpuPredict)
        predictionUpload = model2.predict(uploadPredict)

        print("Previsões cpu:", predictionCPU)
        print("Previsões upload:", predictionUpload)

        arrayCPU.clear()
        arrayRAM.clear()
        arrayUpload.clear()
        arrayDownload.clear()

    try:
        
        writeDB(mediaCpus, dateNow, 1)
        writeDB(frequenciaCpu, dateNow,2)
        writeDB(memPercent, dateNow, 3)
        writeDB(memoryUsed, dateNow, 4)
        writeDB(memoryTotal, dateNow, 5)
        writeDB(diskPercent.percent, dateNow, 6)
        writeDB(diskInput, dateNow, 7)
        writeDB(diskOutput, dateNow, 8)
        writeDB(upload, dateNow, 9)
        writeDB(download, dateNow, 10)

    except mysql.connector.Error as error:
       print("Failed to insert record into table {}".format(error))

    time.sleep(2)