import requests
from base64 import b64encode
from bs4 import BeautifulSoup

def get_alexa_rank(domain):
    url = f"https://www.alexa.com/siteinfo/{domain}"
    response = requests.get(url)

    if response.status_code != 200:
        return None, "Не удалось получить информацию с Alexa."

    soup = BeautifulSoup(response.text, 'html.parser')
    rank_tag = soup.find('div', {'class': 'rankmini'})

    if rank_tag:
        rank_text = rank_tag.text.strip().replace(",", "")
        try:
            return int(rank_text.split(' ')[0]), "Alexa Rank найден."
        except ValueError:
            return None, "Ошибка в извлечении Alexa Rank."
    else:
        return None, "Alexa Rank не найден."


def is_top_1_million(domain):
    rank, message = get_alexa_rank(domain)
    if rank and rank <= 1000000:
        return True, f"Сайт в топ 1 млн Alexa: {rank}"
    else:
        return False, "Сайт не в топ 1 млн Alexa."


MOZ_ACCESS_ID = 'your_access_id'
MOZ_SECRET_KEY = 'your_secret_key'


def get_domain_authority(domain):
    url = "https://lsapi.seomoz.com/v2/url_metrics"
    headers = {
        "Authorization": f"Basic {b64encode(f'{MOZ_ACCESS_ID}:{MOZ_SECRET_KEY}'.encode()).decode()}"
    }

    params = {
        'urls': [f'http://{domain}'],
        'metrics': ['domain_authority']
    }

    response = requests.post(url, headers=headers, json=params)
    if response.status_code != 200:
        return None, "Ошибка при запросе к API Moz."

    data = response.json()
    try:
        da = data[0]['domain_authority']
        return da, f"Domain Authority для {domain}: {da}"
    except KeyError:
        return None, "Не удалось получить Domain Authority."
