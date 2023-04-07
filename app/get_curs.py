import requests


def get_rub(value):
    """функция получения курса"""
    data = requests.get('https://www.cbr-xml-daily.ru/daily_json.js').json()
    result = data['Valute']['USD']['Value']
    return result*value

