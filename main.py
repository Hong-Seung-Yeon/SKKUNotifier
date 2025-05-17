# main.py
import os
import json
from dotenv import load_dotenv
from crawler import scrape_notices
from notifier import send_email

load_dotenv()

SENDER_EMAIL = os.getenv("SENDER_EMAIL")
SENDER_PASSWORD = os.getenv("SENDER_PASSWORD")
RECIPIENT_EMAIL = os.getenv("RECIPIENT_EMAIL")

NOTIFIED_IDS_FILE = "notified_posts.json"

# 이전에 알림 보낸 게시글 ID 불러오기
if os.path.exists(NOTIFIED_IDS_FILE):
    with open(NOTIFIED_IDS_FILE, "r") as f:
        notified_ids = set(json.load(f))
else:
    notified_ids = set()

new_posts = {}

for site_name, base_url in [
    ("소프트웨어학과", "https://cse.skku.edu/cse/notice.do"),
    ("소프트웨어융합대학", "https://sw.skku.edu/sw/notice.do")
]:
    print(f"🌐 {site_name} 공지 수집 중...")
    posts = scrape_notices(site_name, base_url, notified_ids)
    if posts:
        new_posts[site_name] = posts

if new_posts:
    print("📬 새 게시글 발견! 이메일 전송 시작...")
    send_email(new_posts, sender_email=SENDER_EMAIL, sender_password=SENDER_PASSWORD, recipient_email=RECIPIENT_EMAIL)

    # 새로운 ID 저장
    all_ids = notified_ids.union({post['id'] for posts in new_posts.values() for post in posts})
    with open(NOTIFIED_IDS_FILE, "w") as f:
        json.dump(list(all_ids), f)
    print(f"✅ {sum(len(posts) for posts in new_posts.values())}건의 새 게시글 저장 완료.")
else:
    print("🔁 새로운 게시글이 없습니다.")
