# crawler.py (requests + BeautifulSoup 기반)
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

def extract_article_id(url):
    query = parse_qs(urlparse(url).query)
    return query.get("articleNo", [None])[0]

def scrape_notices(site_name, base_url, existing_ids, max_pages=3):
    print(f"\n===== {site_name} 공지사항 =====\n")
    new_posts = []

    for page in range(max_pages):
        offset = page * 10
        url = f"{base_url}?mode=list&articleLimit=10&article.offset={offset}"
        print(f"📄 요청 중: {url}")

        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
        response = requests.get(url, headers=headers)

        if response.status_code != 200:
            print(f"❌ 페이지 로딩 실패: {response.status_code}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")
        titles = soup.select("dt.board-list-content-title a")
        dates = soup.select("dd.board-list-content-info li:nth-of-type(3)")

        if not titles:
            print("⚠️ 게시글 없음 (더 이상 페이지가 없을 수 있음)")
            break

        for tag, date_tag in zip(titles, dates):
            title = tag.get_text(strip=True)
            href = urljoin(base_url, tag.get("href"))
            article_id = extract_article_id(href)
            date = date_tag.get_text(strip=True)

            if article_id in existing_ids:
                continue

            print(f"📌 {title}\n📅 {date}\n🔗 {href}\n\n")
            new_posts.append((article_id, title, href, date))

    return new_posts
