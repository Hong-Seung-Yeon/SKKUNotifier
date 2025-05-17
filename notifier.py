# notifier.py
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(new_posts, sender_email, sender_password, recipient_email):
    subject = "[SKKU 공지] 새로운 게시글이 올라왔습니다!"
    body = ""

    for site_name, posts in new_posts.items():
        body += f"\n📘 {site_name} 공지사항\n"
        for post in posts:
            title = post['title']
            link = post['link']
            date = post.get('date', '')
            body += f"제목: {title}\n게시일: {date}\n링크: {link}\n\n"

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject
    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print("✅ 이메일 전송 완료!")
    except Exception as e:
        print(f"❌ 이메일 전송 실패: {e}")
