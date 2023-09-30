import requests
from requests.auth import HTTPBasicAuth
import json
from jira import JIRA



# TOKEN PARA AUTENTICACAO
jira_token = "ATATT3xFfGF0thDCz5cylZFu9tPG2kDwk5C9Xy9sumeUCbGrUJfKVqNq9SUXzS5xgBxY923Vnh49HwYwqyBslW5ARW51XN9JK3v36b8zwzoXwPCWNnvdYCqBya7drtVhAfsr5T4S4iVfNuqreciuM5cHFk47hOOFduQGtrJpa2t_1WwEZOmzyD8=9FE5A7FB"

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