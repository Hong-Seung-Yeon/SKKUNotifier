# main.py
import json
import os
from dotenv import load_dotenv
from crawler import scrape_notices
from notifier import send_email

# 🔐 환경 변수 로드
load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

NOTIFIED_FILE = "notified_posts.json"

# 기존 게시글 ID 불러오기
if os.path.exists(NOTIFIED_FILE):
    with open(NOTIFIED_FILE, "r") as f:
        notified_ids = set(json.load(f))
else:
    notified_ids = set()

new_posts = {}

# 각 사이트에 대해 크롤링 실행
for site_name, base_url in [
    ("소프트웨어학과", "https://cse.skku.edu/cse/notice.do"),
    ("소프트웨어융합대학", "https://sw.skku.edu/sw/notice.do")
]:
    new_ids_and_posts = []
    ids = []

    posts = scrape_notices(site_name, base_url, notified_ids)
    for post_id, post_title, post_link, post_date in posts:
        ids.append(post_id)
        new_ids_and_posts.append({
            'title': post_title,
            'link': post_link,
            'date': post_date
        })

    if new_ids_and_posts:
        new_posts[site_name] = new_ids_and_posts
        notified_ids.update(ids)

# 새 글이 있으면 메일 전송
if new_posts:
    send_email(
        new_posts,
        sender_email=SENDER_EMAIL,
        sender_password=SENDER_PASSWORD,
        recipient_email=RECIPIENT_EMAIL
    )
    with open(NOTIFIED_FILE, "w") as f:
        json.dump(list(notified_ids), f, indent=2)
    print(f"✅ {sum(len(posts) for posts in new_posts.values())}건의 새 게시글 저장 완료.")
else:
    print("🔁 새로운 게시글이 없습니다.")
