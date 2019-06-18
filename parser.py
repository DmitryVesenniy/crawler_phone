import re
import threading

import requests

PHONE_PATTERN = re.compile(r'(?:\+7|8)\s*(?:[\s\(\)\-]*\d{2,3}){4}', re.VERBOSE)
CAST_PATTERN = (lambda x: re.sub(r"(?:\+7)", "8", x), lambda x: re.sub(r"[\D]", "", x))

LOCK = threading.Lock()


def write_in_console(phone, url):
    global LOCK

    LOCK.acquire()
    print(f"{url} >> {phone}")
    LOCK.release()


def get_numerical_values(txt, url = None):
    phones = set()

    all_phone = PHONE_PATTERN.findall(txt)

    for _phone in all_phone:
        phone = cast_phone(_phone)

        if phone not in phones:
            write_in_console(phone, url)
            phones.add(phone)


def cast_phone(phone):
    for pattern in CAST_PATTERN:
        phone = pattern(phone)

    if len(phone) == 7:
        phone = f"8495{phone}"

    return phone


def worker(url):
    headers = {
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4',
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Accept': 'application/json',
    }

    resp = requests.get(url, headers=headers)

    if resp.ok:
        get_numerical_values(resp.text, url)
