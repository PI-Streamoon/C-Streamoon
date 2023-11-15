import requests
from requests.auth import HTTPBasicAuth
import json
from jira import JIRA



# TOKEN PARA AUTENTICACAO
jira_token = "ATCTT3xFfGN0L_I4FQKEN9U2RHRkHfiQYxw35GCv4icYNm6gAZh3QQ8f2KMOxyXZ0g7Gwl1V_qbWY13fmfz83-f7qVNzwhDT3w9bEW6fJvUPDq0dHf4_tAhc7FtYWvxaG3ALfKdG32y5_AY1-wsuhV-K3U1TvKnLs0p6wBtzDIzoTBzaBxn5NJ8=14EFDB67"

# CREDENCIAIS PARA AUTENTICAÇÃO
url = "https://streamsecure.atlassian.net/rest/api/3/issue"
server_name = "https://streamsecure.atlassian.net"
email = "suportestreamoon@gmail.com"

jira_connection = JIRA(
  basic_auth=(email, jira_token),
  server=server_name
)

def chamado(mensagem, descricao):
  issue_dict = {
    'project': {'key': 'STREAM'},
    'summary': mensagem,
    'description': descricao,
    'issuetype': {'name':'[System] Incident'},
  }

  new_issue = jira_connection.create_issue(fields=issue_dict)
  print(new_issue)