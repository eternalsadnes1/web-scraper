# main.py
import pandas as pd
import schedule
import time
from datetime import datetime

# Импортируем наши настройки и функции скрейперов
import config
from scrapers import price_scraper, news_scraper


def run_price_monitoring():
    """Запускает задачу мониторинга цен."""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запуск мониторинга цен...")

    price_data = []
    for name, url in config.PRICE_TRACKER_URLS.items():
        product_name, price = price_scraper.get_price(name, url, config.HEADERS)
        if price is not None:
            price_data.append({
                'timestamp': datetime.now(),
                'product': product_name,
                'price': price,
                'url': url
            })
            # Проверка на пороговое значение
            if product_name in config.PRICE_ALERT_THRESHOLD and price < config.PRICE_ALERT_THRESHOLD[product_name]:
                print(f"!!! ВНИМАНИЕ: Цена на '{product_name}' упала ниже порога: {price} руб. !!!")

    if not price_data:
        print("Не удалось собрать данные о ценах.")
        return

    # Сохраняем данные в CSV
    df = pd.DataFrame(price_data)
    try:
        df.to_csv('data/prices.csv', mode='a', header=not pd.io.common.file_exists('data/prices.csv'), index=False,
                  encoding='utf-8-sig')
        print("Данные о ценах успешно сохранены в data/prices.csv")
    except Exception as e:
        print(f"Ошибка сохранения файла: {e}")


def run_news_aggregation():
    """Запускает задачу сбора новостей."""
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Запуск сбора новостей...")

    all_filtered_news = []
    for name, url in config.NEWS_URLS.items():
        news = news_scraper.get_news(name, url, config.NEWS_KEYWORDS, config.HEADERS)
        all_filtered_news.extend(news)

    if not all_filtered_news:
        print("Не найдено новостей по ключевым словам.")
        return

    # Сохраняем новости в CSV
    df = pd.DataFrame(all_filtered_news)
    df.to_csv('data/filtered_news.csv', index=False, encoding='utf-8-sig')
    print(f"Найдено и сохранено {len(all_filtered_news)} новостей в data/filtered_news.csv")
    for item in all_filtered_news:
        print(f"- {item['source']}: {item['title']}")


# --- Настройка расписания ---
print("Веб-скрейпер запущен. Ожидание запланированных задач...")

# Запускаем задачи один раз при старте
run_price_monitoring()
run_news_aggregation()

# Настраиваем расписание
schedule.every(4).hours.do(run_price_monitoring)  # Проверять цены каждые 4 часа
schedule.every().day.at("09:00").do(run_news_aggregation)  # Собирать новости каждое утро в 9:00

# Бесконечный цикл для выполнения задач по расписанию
while True:
    schedule.run_pending()
    time.sleep(1)