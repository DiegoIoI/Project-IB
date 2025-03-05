import whois
import datetime
from urllib.parse import urlparse

def is_known_payment_service(domain):
    known_services = ["yookassa", "tinkoff", "qiwi", "pay", "sberbank"]
    return any(service in domain for service in known_services)

def check_domain(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    if is_known_payment_service(domain):
        return True
    else:
        return False

def get_domain_age(domain):
    try:
        w = whois.whois(domain)
        creation_date = w.creation_date

        if isinstance(creation_date, list):
            creation_date = creation_date[0]
        
        if creation_date:
            age = (datetime.datetime.now() - creation_date).days / 365
            return age
        else:
            return None
    except Exception as e:
        return None


def check_https(url):
    if url.startswith("https://"):
        return True, "Ссылка использует HTTPS."
    else:
        return False, "URL не использует HTTPS. Это может быть опасным."


def check_domain_length(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc

    domain_length = len(domain)
    if domain_length < 3:
        return False, "Домен слишком короткий. Это может быть фишинг."
    elif domain_length > 253:
        return False, "Домен слишком длинный. Это может быть подозрительным."
    
    return True, "Домен имеет нормальную длину."
