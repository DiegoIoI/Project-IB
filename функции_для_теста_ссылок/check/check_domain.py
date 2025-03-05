import re
import ssl
import socket
from urllib.parse import urlparse
import requests

def check_suspicious_characters(domain):
    if re.search(r'\d', domain):  # Проверяем наличие цифр в домене
        return False, "Домен содержит цифры, что может быть подозрительно."
    if re.search(r'[-]{2,}', domain):  #Проверяем наличие нескольких дефисов подряд
        return False, "Домен содержит несколько дефисов подряд, что может быть подозрительно."
    return True, "Домен не содержит подозрительных символов."


def check_subdomains(url):
    parsed_url = urlparse(url)
    subdomains = parsed_url.netloc.split(".")[:-2]  #Извлекаем поддомены
    if len(subdomains) > 2:  #Если поддоменов больше 2-х
        return False, "Слишком много поддоменов, это может быть фишинг."
    return True, "Поддомены в порядке."


def check_ssl(url):
    parsed_url = urlparse(url)
    hostname = parsed_url.netloc
    try:
        ssl_info = ssl.create_default_context().wrap_socket(socket.socket(), server_hostname=hostname)
        ssl_info.connect((hostname, 443))
        ssl_info.close()
        return True, "SSL-сертификат действителен."
    except Exception as e:
        return False, "SSL-сертификат недействителен."

def check_google_safe_browsing(url):
    api_key = 'YOUR_GOOGLE_API_KEY'
    endpoint = f'https://safebrowsing.googleapis.com/v4/threatMatches:find?key={api_key}'
    body = {
        'client': {
            'clientId': 'yourCompany',
            'clientVersion': '1.0.0'
        },
        'threatInfo': {
            'threatTypes': ['MALWARE', 'SOCIAL_ENGINEERING'],
            'platformTypes': ['ANY_PLATFORM'],
            'urlInfo': {
                'urls': [url]
            }
        }
    }
    response = requests.post(endpoint, json=body)
    data = response.json()
    if 'matches' in data:
        return False, "Этот сайт находится в черном списке Google Safe Browsing."
    return True, "Этот сайт безопасен по версии Google Safe Browsing."
