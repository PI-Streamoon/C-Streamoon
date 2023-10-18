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
    "MemoryPercent" : [],
    "MemoryUsed" : [],
    "MemoryTotal" : [],
    "Disk" : [],
    "Upload": [],
    "Download": []
}
cpuQuantity = psutil.cpu_count(logical=True)
for i in range(cpuQuantity):
    cpuName = (f"CPU{i+1}")
    consoleData[cpuName] = []


# Capturar os dados de CPU/RAM/DISK/UPLOAD/DOWNLOAD a cada 2segs
while True:

    cpusPercent = psutil.cpu_percent(interval=1, percpu=True)

    memory = (psutil.virtual_memory())
    memPercent = memory.percent
    memoryUsed = round((memory.used / 1024 / 1024 / 1000), 1)   
    memoryTotal = round((memory.total / 1024 / 1024 / 1000), 1)
    upload = round((psutil.net_io_counters().bytes_sent / 1e6),1)
    download = round((psutil.net_io_counters().bytes_recv / 1e6),1)

    diskPartitions = psutil.disk_partitions()
    diskPercent = psutil.disk_usage(diskPartitions[0].mountpoint)                      


    somaCpus = 0
    mediaCpus = 0
    for i in range(psutil.cpu_count()):
        somaCpus += cpusPercent[i]
        cpuName1 = (f"CPU{i+1}") 
        consoleData[cpuName1].append(cpusPercent[i])
    mediaCpus = somaCpus / len(cpusPercent)


    dateNow = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    indexHour.append(dateNow)

    systemClear = ('clear' if platform.system() == 'Linux' else 'cls')
    os.system(systemClear)

    showText()
    consoleData["MemoryPercent"].append(memPercent)
    consoleData["MemoryUsed"].append(memoryUsed)
    consoleData["MemoryTotal"].append(memoryTotal)
    consoleData["Disk"].append(diskPercent.percent)
    consoleData["Upload"].append(upload)
    consoleData["Download"].append(download)
    
    #Integração slack!
    mensagemSlack = ""
    if (memPercent > 80):
        connectionJira.chamado("Crítico", "A MEMORIA VIRTUAL ESTÁ ACIMA DE 80%")

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
                            "text": "*A MEMORIA VIRTUAL ESTÁ ACIMA DE 80%*"
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
       
        
    for i in range(len(cpusPercent)):
        if int(cpusPercent[i])> 90:
            connectionJira.chamado("Crítico", "O CPU VIRTUAL ESTÁ ACIMA DE 90%")

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
					"text": f"*O CPU VIRTUAL {i} ESTÁ ACIMA DE 90%*"
				}
			]
		},
		{
			"type": "divider"
		}
	]}
        suporte = "https://hooks.slack.com/services/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"
        #postMsg = requests.post(suporte, data=json.dumps(mensagemSlack))
        
           
    if (mediaCpus> 90):
        connectionJira.chamado("Crítico", "A SUA MÉDIA DE CPU ULTRAPASSOU 90%")

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
					"text": f"*A SUA MÉDIA DE CPU ULTRAPASSOU 90%*"
				}
			]
		},
		{
			"type": "divider"
		}
	]}
        suporte = "https://hooks.slack.com/services/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"
        #postMsg = requests.post(suporte, data=json.dumps(mensagemSlack))
    
    if (download < 100):
        #connectionJira.chamado("Crítico", "A SUA ENTRADA DE REDE (DOWNLOAD) ESTÁ ABAIXO DE 100Mb")
        
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
					"text": f"*A SUA ENTRADA DE REDE (DOWNLOAD) ESTÁ ABAIXO DE 100Mb*"
				}
			]
		},
		{
			"type": "divider"
		}
	]}
        suporte = "https://hooks.slack.com/services/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"
        #postMsg = requests.post(suporte, data=json.dumps(mensagemSlack))

    if (upload < 40):
        #connectionJira.chamado("Crítico", "A SUA SAÍDA DE REDE (UPLOAD) ESTÁ ABAIXO DE 40Mb")
        
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
					"text": f"*A SUA SAÍDA DE REDE (UPLOAD) ESTÁ ABAIXO DE 40Mb*"
				}
			]
		},
		{
			"type": "divider"
		}
	]}
        suporte = "https://hooks.slack.com/services/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"
        #postMsg = requests.post(suporte, data=json.dumps(mensagemSlack))
    
    df = pd.DataFrame(data=consoleData, index=indexHour)
    print(f"\n{df}")


    connection = mysql.connector.connect(
        host='localhost',
        database='streamoon',
        user='StreamoonUser',
        password='Moon2023'
    )

    try:
        
        mySql_insert_query_cpu_percent = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(mediaCpus) + ", '" + str(dateNow) + "', 1);"
        mySql_insert_query_memory = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(memPercent) + ", '" + str(dateNow) + "', 2);"
        mySql_insert_query_memory_used = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(memoryUsed) + ", '" + str(dateNow) + "', 3);"
        mySql_insert_query_memory_total = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(memoryTotal) + ", '" + str(dateNow) + "', 4);"
        mySql_insert_query_disc_percent = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(diskPercent.percent) + ", '" + str(dateNow) + "', 5);"
        mySql_insert_query_upload = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(upload) + ", '" + str(dateNow) + "', 6);"
        mySql_insert_query_download = "INSERT INTO registro (idRegistro, registro, dtHora, fkComponenteServidor) VALUES (null, " + str(download) + ", '" + str(dateNow) + "', 7);"

        cursor = connection.cursor()
        cursor.execute(mySql_insert_query_cpu_percent)
        cursor.execute(mySql_insert_query_memory)
        cursor.execute(mySql_insert_query_memory_used)
        cursor.execute(mySql_insert_query_memory_total)
        cursor.execute(mySql_insert_query_disc_percent)
        cursor.execute(mySql_insert_query_download)
        cursor.execute(mySql_insert_query_upload)
                      

        connection.commit()
        cursor.close()


    except mysql.connector.Error as error:
       print("Failed to insert record into Laptop table {}".format(error))

    time.sleep(2)
    

if connection.is_connected():
    connection.close()
    
    
    
    
    
    

