import requests
from requests.auth import HTTPBasicAuth
import json
from jira import JIRA

# TOKEN PARA AUTENTICACAO
jira_token = "ATCTT3xFfGN09vXbqwNE2N6w4xQ-_6HaBdmR7iynnQYqN_fok5gSLAbAZYgSQ81uU3nilCiKiyAv12ofnunvh2XpNffUfRFN6y95hm5tJaKll3-Xvxpx6AwwK-gfwM88pDL_OhHi340bvdYZusm7Ly2vIjN4wawHUVX34Ovw_jjusOeqPv7Uxek=DE9803F9"

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