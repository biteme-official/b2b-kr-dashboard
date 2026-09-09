"""로컬 개발 서버 — Vercel CLI/계정 없이 대시보드를 그대로 실행한다.

    python dev_server.py        # http://localhost:3000

index.html 등 정적 파일을 서빙하고, /api/data 는 Vercel에 배포되는 것과
동일한 api/data.py 의 handler 를 그대로 호출한다.

고도몰 키는 .env 파일(GODO_PARTNER_KEY, GODO_API_KEY)에서 읽는다.
"""

import os
import sys
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).parent
PORT = int(os.environ.get("PORT", "3000"))


def load_env():
    """.env / .env.local 을 os.environ 에 로드 (이미 설정된 값은 유지)."""
    for name in (".env", ".env.local"):
        path = ROOT / name
        if not path.exists():
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line or line.startswith("#") or "=" not in line:
                continue
            key, _, val = line.partition("=")
            os.environ.setdefault(key.strip(), val.strip().strip('"').strip("'"))


load_env()

if not os.environ.get("GODO_API_KEY"):
    print("WARN: GODO_API_KEY not set - check your .env file", file=sys.stderr)

sys.path.insert(0, str(ROOT / "api"))
import data as api_data  # noqa: E402


class DevHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        if self.path.split("?")[0].rstrip("/") == "/api/data":
            # 배포본과 동일한 handler 를 현재 커넥션 위에서 실행
            api_data.handler.do_GET(self)
            return
        super().do_GET()

    def log_message(self, fmt, *args):
        sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))


if __name__ == "__main__":
    print(f"Dev server: http://localhost:{PORT}  (Ctrl+C to stop)", flush=True)
    ThreadingHTTPServer(("127.0.0.1", PORT), DevHandler).serve_forever()
