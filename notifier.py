# notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(posts_by_site, sender_email, sender_password, recipient_email):
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = "📢 [SKKU 공지] 신규 공지글 안내"

    body = ""
    for site, posts in posts_by_site.items():
        body += f"< {site} >\n\n"
        for post in posts:
            body += f"📌 {post['title']}\n📅 게시일: {post['date']}\n🔗 링크: {post['link']}\n\n"

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender_email, sender_password)
            server.send_message(msg)
        print("이메일 전송 완료!")
    except Exception as e:
        print(f"이메일 전송 실패: {e}")
