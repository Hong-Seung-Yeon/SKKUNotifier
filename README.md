# SKKU Notifier

성균관대학교 소프트웨어학과 / 소프트웨어융합대학 공지사항을 자동으로 수집하여 이메일로 보내주는 Python 기반 자동화 프로젝트입니다. 

무료 클라우드 플랫폼 **Render.com**과 **cron-job.org**를 활용하여 별도의 서버나 유료 서비스 없이 매일 새로운 공지를 받아볼 수 있습니다.

---

## 기능 요약

- 소프트웨어학과 / 소프트웨어융합대학 공지사항 크롤링
- 게시글 ID 기준 중복 방지 (알림 전송 여부 저장)
- 새로운 게시글이 있을 때만 Gmail로 메일 전송
- FastAPI 기반 웹 서버를 통해 `/run` 경로로 실행 가능
- Render.com 배포 및 cron-job.org 연동으로 완전 자동화

---

## 프로젝트 구조

```
SKKUNotifier/
├── main.py              # 공지 수집 및 메일 전송 실행 로직
├── crawler.py           # 공지사항 크롤러
├── notifier.py          # 이메일 전송 함수
├── server.py            # FastAPI 엔드포인트 (/run)
├── requirements.txt     # 필요한 패키지 목록
├── notified_posts.json  # 이미 알림 보낸 게시글 ID 저장 (Render에선 휘발성)
└── .env (로컬 전용)     # 이메일 환경 변수 저장
```

---

## 실행 흐름

1. `/run` 경로로 GET 요청
2. `server.py`가 `main.py`를 subprocess로 실행
3. `main.py`는 두 학과 공지를 크롤링하여 새 게시글 판별
4. 새 글이 있다면 `notifier.py`를 통해 메일 발송
5. 결과는 Render 로그 및 `/run` 응답에서 확인 가능


---

## Build Command

```bash
pip install -r requirements.txt
```

---

## 로컬 테스트 방법

```bash
uvicorn server:app --reload
```

접속:
- [http://127.0.0.1:8000/run](http://127.0.0.1:8000/run)

---

## 자동 실행 설정

### ✅ Render 설정 (https://render.com)

Render는 코드를 클라우드에서 자동으로 실행할 수 있는 플랫폼입니다. SKKU Notifier는 Render의 Web Service (Free 플랜)을 사용해 배포됩니다.

#### Render 생성 시 필수 입력 항목:

| 항목              | 입력값 또는 예시                                               |
|-------------------|------------------------------------------------------------------|
| **Name**           | skkunotifier                                                    |
| **Build Command**  | `pip install -r requirements.txt`                               |
| **Start Command**  | `uvicorn server:app --host 0.0.0.0 --port 10000`               |

---

## 환경변수 설정 (Render 대시보드)

Render.com의 Environment Variables 탭에서 아래 항목 추가:

| Key               | Value                             | 설명                     |
|------------------|-----------------------------------|--------------------------|
| `SENDER_EMAIL`    | Gmail 주소                         | 메일을 보낼 계정 주소     |
| `SENDER_PASSWORD` | Gmail 앱 비밀번호                  | 앱 비밀번호 사용 필수     |
| `RECIPIENT_EMAIL` | 수신 받을 이메일 주소              | 알림을 받을 대상 이메일   |

> ⚠️ Gmail은 반드시 [앱 비밀번호](https://support.google.com/accounts/answer/185833?hl=ko) 사용 필요

> ⚠️ **Render Free Web Service는 트래픽이 없으면 약 15분 후 자동으로 중단(suspended)** 됩니다.
>
> 서버가 중단된 상태에서는 `/run` 호출이 처음에 느릴 수 있습니다.

관련 문서: [Render 공식 문서 - Free Web Services](https://render.com/docs/free)

---

### ✅ cron-job.org 설정 (https://cron-job.org)

cron-job.org는 무료로 HTTP 요청을 정기적으로 수행해주는 서비스입니다. Render 서버가 꺼지지 않도록 **10분 간격**으로 `/run` 엔드포인트를 호출하게 설정할 수 있습니다.

설정 방법:

1. 회원가입 후 로그인
2. 새 Cronjob 생성 클릭
3. 다음 정보 입력:

| 항목         | 설정값                                      |
|--------------|----------------------------------------------|
| URL          | `https://skkunotifier.onrender.com/run`     |
| Schedule     | **Every 10 minutes**                         |

> 이렇게 설정하면 Render 서버가 **수시로 깨어 있는 상태를 유지**할 수 있으며, 공지가 있을 경우 알림 메일이 자동 발송됩니다.

---

## 주의사항 (Render 파일 저장소)

- `notified_posts.json`은 Render 서버가 재시작되면 **사라짐**
- 매 실행마다 모든 글이 새 글로 인식되어 메일이 중복 전송될 수 있음
- 실제 서비스에는 Supabase, Firebase, AWS S3 등 외부 저장소 연동 추천

---

## 향후 개선 아이디어

- DB 연동으로 게시글 ID 영구 저장
- HTML 메일 포맷 적용 (스타일, 링크 강조 등)
- GPT API 연결해 요약

---

## 라이선스

MIT License
