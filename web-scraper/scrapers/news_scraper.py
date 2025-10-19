# scrapers/news_scraper.py
import requests
from bs4 import BeautifulSoup
import time

# Опять же, селекторы - это примеры для демонстрации
NEWS_SELECTORS = {
    'habr.com': {
        'container': 'article.tm-articles-list__item',
        'title': 'a.tm-title__link',
        'link': 'a.tm-title__link'
    },
    'www.rbc.ru': {
        'container': 'div.js-news-feed-item',
        'title': 'span.news-feed__item__title',
        'link': 'a.news-feed__item__link'
    }
}


def get_news(site_name, url, keywords, headers):
    """Сбор и фильтрация новостей с одного сайта."""
    try:
        domain = url.split('/')[2]
        if domain not in NEWS_SELECTORS:
            print(f"Нет селекторов для {domain}")
            return []

        response = requests.get(url, headers=headers)
        response.raise_for_status()
        time.sleep(2)

        soup = BeautifulSoup(response.text, 'lxml')
        config = NEWS_SELECTORS[domain]

        articles = soup.select(config['container'])
        filtered_news = []

        for article in articles:
            title_element = article.select_one(config['title'])
            link_element = article.select_one(config['link'])

            if not title_element or not link_element:
                continue

            title = title_element.text.strip()
            link = link_element.get('href', '')

            # Корректируем относительные ссылки
            if not link.startswith('http'):
                link = f"https://{domain}{link}"

            # Проверяем, есть ли ключевые слова в заголовке
            if any(keyword.lower() in title.lower() for keyword in keywords):
                filtered_news.append({'source': site_name, 'title': title, 'link': link})

        return filtered_news

    except Exception as e:
        print(f"Ошибка при сборе новостей с {site_name}: {e}")
        return []