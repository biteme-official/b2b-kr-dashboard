# B2B KR Dashboard

바잇미 국내 B2B(도매) 매출 대시보드. 고도몰 OpenHub API에서 주문 데이터를 실시간 조회해 KPI·차트로 시각화합니다.

## 접속 주소

| 용도 | 주소 | 로그인 |
|---|---|---|
| **프로덕션** | https://b2b-kr-dashboard.vercel.app | 불필요 |
| 브랜치 프리뷰 | `b2b-kr-dashboard-git-<branch>-biteme.vercel.app` | Vercel 로그인 필요 |
| 배포별 프리뷰 | PR에 자동으로 코멘트되는 URL | Vercel 로그인 필요 |

> ⚠️ `biteme-official.github.io/b2b-kr-dashboard` 는 **사용하지 않습니다.** 과거 GitHub Pages 흔적이며, `/api/data`가 없어 데이터가 뜨지 않습니다.

프리뷰 URL은 Vercel Deployment Protection(SSO)이 걸려 있어 **Vercel `biteme` 팀 멤버**만 열 수 있습니다. 팀 멤버가 아니면 로컬(`python dev_server.py`)에서 확인하고, 프리뷰 확인이 필요한 PR은 관리자에게 요청하세요.

## 구조

```
index.html        대시보드 UI 전체 (단일 파일, Chart.js CDN)
api/data.py       Vercel Python 서버리스 함수 — 고도몰 주문 조회 + 집계
dev_server.py     로컬 개발 서버 (Vercel CLI 없이 실행)
vercel.json       Vercel 설정
requirements.txt  Python 의존성
```

브라우저가 `/api/data`를 호출 → `api/data.py`가 고도몰 `Order_Search` API를 14일 배치·5스레드 병렬로 조회 → JSON 반환 → 화면 렌더링. 5분마다 자동 갱신됩니다.

## 로컬 개발

**Vercel 계정 없이 실행합니다.** Python만 있으면 됩니다.

```bash
git clone https://github.com/biteme-official/b2b-kr-dashboard
cd b2b-kr-dashboard

pip install -r requirements.txt

cp .env.example .env               # 관리자에게 받은 고도몰 키를 채워넣기

python dev_server.py               # http://localhost:3000
```

`dev_server.py`는 정적 파일을 서빙하고 `/api/data`를 **배포본과 동일한 `api/data.py` handler**로 처리합니다. 포트 변경은 `PORT=4000 python dev_server.py`.

정상 동작 시 `/api/data`가 200과 함께 약 1MB의 JSON을 반환합니다(최초 호출 ~8초, 이후 5분간 캐시).

> `python -m http.server` 등 단순 정적 서버로는 **동작하지 않습니다.** `/api/data`를 처리하지 못해 화면이 로딩에서 멈춥니다.

### Vercel CLI를 쓰는 경우 (선택)

Vercel `biteme` 팀 멤버라면 실제 런타임과 동일한 환경으로 띄울 수 있습니다.

```bash
python -m pip install uv           # ★ Windows 필수 — 트러블슈팅 참고
vercel link                        # biteme 팀 → b2b-kr-dashboard
vercel env pull
vercel dev
```

팀 멤버가 아니면 위 명령들은 실패합니다. `dev_server.py`를 사용하세요.

## 배포

`master` 브랜치에 push하면 Vercel Git 연동으로 **자동 배포**됩니다. 별도 배포 명령이나 GitHub Actions는 없습니다.

작업 흐름:

```bash
git switch -c feat/my-change
# 수정 후
git push -u origin feat/my-change
# GitHub에서 PR 생성 → 리뷰 → master 머지 → 자동 배포
```

## 환경변수

| 이름 | 용도 |
|---|---|
| `GODO_PARTNER_KEY` | 고도몰 OpenHub 파트너 키 |
| `GODO_API_KEY` | 고도몰 OpenHub API 키 |

Vercel의 Production / Preview / Development 3개 환경에 모두 등록돼 있습니다.

로컬에서는 `.env` 파일에 직접 넣습니다(`.env.example` 참고). 키 값은 관리자(bmahsang / bmhayoung)에게 요청하세요. Vercel 팀 멤버라면 `vercel env pull`로 받아도 됩니다.

> 🔒 이 키는 **주문 원본 데이터(주문자명·회원ID 등 개인정보 포함)** 조회 권한을 가집니다. `.env`를 공유하거나 커밋하지 마세요. `.gitignore`에 `.env*`가 등록돼 있습니다.

## 트러블슈팅

**`Failed to install or locate uv` / `uv is required for this project`** (`vercel dev` 사용 시)

Windows에서 `python3` 명령이 MS 스토어 스텁으로 잡혀 Vercel의 uv 자동 설치가 실패합니다. 직접 설치하세요:

```bash
python -m pip install uv
```

**`WARN: GODO_API_KEY not set`**

`.env` 파일이 없거나 값이 비어 있습니다. `.env.example`을 복사해 채우세요.

**`/api/data`가 500을 반환**

서버 콘솔 로그에 실제 원인이 출력됩니다. 대부분 환경변수 누락 또는 고도몰 API 응답 문제입니다.

**프리뷰 URL이 Vercel 로그인 화면으로 넘어감**

Vercel `biteme` 팀 멤버가 아닌 계정입니다. 팀 계정은 별도로 배포하지 않으므로, 로컬(`python dev_server.py`)에서 확인한 뒤 PR을 올리면 됩니다. 프리뷰 확인이 꼭 필요하면 관리자에게 요청하세요.
