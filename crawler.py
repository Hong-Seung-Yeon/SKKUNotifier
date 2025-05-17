# crawler.py
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

def scrape_notices(site_name, base_url, notified_ids):
    headers = {"User-Agent": "Mozilla/5.0"}
    new_posts = []

    for offset in range(0, 30, 10):
        url = f"{base_url}?mode=list&articleLimit=10&article.offset={offset}"
        print(f"요청 중: {url}")

        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
        except Exception as e:
            print(f"❌ [{site_name}] 요청 실패: {e}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")
        notice_items = soup.select("ul.board-list-wrap > li")

        for item in notice_items:
            title_tag = item.select_one(".board-list-content-title a")
            date_tag = item.select_one(".board-list-content-info li:nth-child(3)")

            if not title_tag:
                continue

            post_title = title_tag.get_text(strip=True)
            post_link = urljoin(base_url, title_tag['href'])
            post_id = post_link.split("articleNo=")[-1].split("&")[0]
            post_date = date_tag.get_text(strip=True) if date_tag else "N/A"

            if post_id not in notified_ids:
                new_posts.append({
                    "id": post_id,
                    "title": post_title,
                    "link": post_link,
                    "date": post_date
                })

    return new_posts
