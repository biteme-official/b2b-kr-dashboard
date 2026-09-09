# B2B KR Dashboard

바잇미 국내 B2B(도매) 매출 대시보드. 고도몰 OpenHub API에서 주문 데이터를 실시간 조회해 KPI·차트로 시각화합니다.

## 접속 주소

| 용도 | 주소 | 로그인 |
|---|---|---|
| **프로덕션** | https://b2b-kr-dashboard.vercel.app | 불필요 |
| 브랜치 프리뷰 | `b2b-kr-dashboard-git-<branch>-biteme.vercel.app` | Vercel 로그인 필요 |
| 배포별 프리뷰 | PR에 자동으로 코멘트되는 URL | Vercel 로그인 필요 |

> ⚠️ `biteme-official.github.io/b2b-kr-dashboard` 는 **사용하지 않습니다.** 과거 GitHub Pages 흔적이며, `/api/data`가 없어 데이터가 뜨지 않습니다.

프리뷰 URL은 Vercel Deployment Protection(SSO)이 걸려 있어 **Vercel `biteme` 팀 멤버**만 열 수 있습니다. 열리지 않으면 팀 초대를 요청하세요.

## 구조

```
index.html        대시보드 UI 전체 (단일 파일, Chart.js CDN)
api/data.py       Vercel Python 서버리스 함수 — 고도몰 주문 조회 + 집계
vercel.json       Vercel 설정
requirements.txt  Python 의존성
```

브라우저가 `/api/data`를 호출 → `api/data.py`가 고도몰 `Order_Search` API를 14일 배치·5스레드 병렬로 조회 → JSON 반환 → 화면 렌더링. 5분마다 자동 갱신됩니다.

## 로컬 개발

### 사전 준비 (최초 1회)

```bash
git clone https://github.com/biteme-official/b2b-kr-dashboard
cd b2b-kr-dashboard

python -m pip install uv          # ★ 필수 — 아래 트러블슈팅 참고
pip install -r requirements.txt

vercel link                        # biteme 팀 → b2b-kr-dashboard 선택
vercel env pull                    # .env.local 생성 (고도몰 키)
```

필요 버전: Node 20+, Python 3.9+, Vercel CLI

### 실행

```bash
vercel dev        # http://localhost:3000
```

`python -m http.server` 등 정적 서버로는 **동작하지 않습니다.** `/api/data`가 서버리스 함수라 `vercel dev`가 필요합니다.

정상 동작 시 `/api/data`가 200과 함께 약 1MB의 JSON을 반환합니다(최초 호출 ~10초).

## 배포

`master` 브랜치에 push하면 Vercel Git 연동으로 **자동 배포**됩니다. 별도 배포 명령이나 GitHub Actions는 없습니다.

작업 흐름:

```bash
git switch -c feat/my-change
# 수정 후
git push -u origin feat/my-change
# GitHub에서 PR 생성 → 프리뷰 URL로 확인 → master 머지 → 자동 배포
```

## 환경변수

| 이름 | 용도 |
|---|---|
| `GODO_PARTNER_KEY` | 고도몰 OpenHub 파트너 키 |
| `GODO_API_KEY` | 고도몰 OpenHub API 키 |

Production / Preview / Development 3개 환경에 모두 등록돼 있습니다. 로컬에서는 `vercel env pull`로 받으세요.

> 🔒 이 키는 **주문 원본 데이터(주문자명·회원ID 등 개인정보 포함)** 조회 권한을 가집니다. `.env.local`을 공유하거나 커밋하지 마세요. `.gitignore`에 `.env*`가 등록돼 있습니다.

## 트러블슈팅

**`Failed to install or locate uv` / `uv is required for this project`**

Windows에서 `python3` 명령이 MS 스토어 스텁으로 잡혀 Vercel의 uv 자동 설치가 실패합니다. 직접 설치하세요:

```bash
python -m pip install uv
```

**`/api/data`가 500을 반환**

`vercel dev` 콘솔 로그에 실제 원인이 출력됩니다. 대부분 uv 미설치 또는 환경변수 누락입니다.

**프리뷰 URL이 Vercel 로그인 화면으로 넘어감**

Vercel `biteme` 팀에 초대되지 않은 계정입니다. 팀 관리자에게 초대를 요청하세요.
