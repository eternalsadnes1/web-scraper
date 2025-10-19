# config.py

# 1. URL для отслеживания курсов валют 💵 💶
# Примечание: Источником является главная страница ЦБ РФ.
# Скрейперу нужно будет найти на ней таблицу с курсами и извлечь строки для 'USD', 'EUR' и 'CNY'.
CURRENCY_URL = 'https://www.cbr.ru/'

# 2. URLs для мониторинга цен на MacBook Air M2 256GB 💻
# Ключ - уникальное название товара, значение - URL для парсинга.
# ВАЖНО: URL-адреса могут устареть. Перед запуском проверьте их актуальность.
PRICE_TRACKER_URLS = {
    'MacBook Air M2 256GB (М.Видео)': 'https://www.mvideo.ru/products/noutbuk-apple-macbook-air-13-m2-256gb-space-gray-mlxy3rua-30064788',
    'MacBook Air M2 256GB (DNS)': 'https://www.dns-shop.ru/product/43a5f70d473fed20/136-noutbuk-apple-macbook-air-m2-seryj/',
    'MacBook Air M2 256GB (Ozon)': 'https://www.ozon.ru/product/noutbuk-apple-macbook-air-13-6-m2-8-256-gb-2022-588288302/',
}

# 3. Пороговая цена для уведомлений (в рублях)
# Если цена опустится ниже этого значения, вы получите уведомление.
PRICE_ALERT_THRESHOLD = {
    # Для каждого товара из списка PRICE_TRACKER_URLS можно задать свой порог
    'MacBook Air M2 256GB (М.Видео)': 95000,
    'MacBook Air M2 256GB (DNS)': 95000,
    'MacBook Air M2 256GB (Ozon)': 93000,
}

# 4. Сайты для сбора новостей (оставляем для примера) 📰
NEWS_URLS = {
    'Habr': 'https://habr.com/ru/feed/',
    'РБК': 'https://www.rbc.ru/',
}

# 5. Ключевые слова для фильтрации новостей
NEWS_KEYWORDS = ['python', 'ии', 'анализ данных', 'экономика', 'ноутбуки']

# 6. Общие заголовки для всех HTTP-запросов 🌐
# Это помогает имитировать запрос от реального браузера и снижает риск блокировки.
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}