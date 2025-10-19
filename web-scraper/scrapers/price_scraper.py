# scrapers/price_scraper.py
import requests
from bs4 import BeautifulSoup
import time

# Важно! Эти селекторы являются примерами и почти наверняка потребуют обновления.
# Структура сайтов постоянно меняется.
SELECTORS = {
    'www.ozon.ru': {'tag': 'span', 'class_': 'k9l l9k'},  # Пример
    'www.dns-shop.ru': {'tag': 'div', 'class_': 'product-buy__price'},  # Пример
}


def get_price(name, url, headers):
    """Основная функция для получения цены с одной страницы."""
    try:
        # Определяем, для какого сайта мы ищем селектор
        domain = url.split('/')[2]
        if domain not in SELECTORS:
            print(f"Внимание: Для домена {domain} не задан селектор. Пропускаем.")
            return None, None

        # Отправляем запрос
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Проверяем статус ответа

        time.sleep(2)  # Вежливая задержка между запросами

        soup = BeautifulSoup(response.text, 'lxml')

        # Ищем цену по заданному селектору
        selector_info = SELECTORS[domain]
        price_element = soup.find(selector_info['tag'], class_=selector_info['class_'])

        if not price_element:
            print(f"Не удалось найти цену для '{name}' по URL: {url}")
            return name, None

        # Очищаем цену от лишних символов (₽, пробелы)
        price_text = ''.join(filter(str.isdigit, price_element.text))

        return name, int(price_text)

    except requests.exceptions.RequestException as e:
        print(f"Ошибка сети при запросе {url}: {e}")
        return name, None
    except Exception as e:
        print(f"Непредвиденная ошибка при парсинге {url}: {e}")
        return name, None