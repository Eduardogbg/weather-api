"""
    Responsável por toda interação com a API climatempo
"""

import requests

BASE_URL = 'http://apiadvisor.climatempo.com.br/'
TOKEN = '0dbe332e49706163db8b4cf1e7b08742'


def assemble_req_url(code):
    """
        Retorna a URL do endpoint da API
    """

    return BASE_URL + '/api/v1/forecast/locale/' + str(code) + '/days/15?token=' + TOKEN


def get_request(code):
    """
        Faz um GET com os parâmetros adequados e retorna um JSON
    """

    url = assemble_req_url(code)
    return requests.get(url).json()
