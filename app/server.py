import json
from http import HTTPStatus
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import parse_qs, urlparse

from .engine import build_item_similarity, build_matrices, recommend

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_PATH = BASE_DIR / "data" / "interactions.json"
WEB_DIR = BASE_DIR / "web"


def load_interactions():
    if not DATA_PATH.exists():
        return []
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_interactions(rows):
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(rows, indent=2), encoding="utf-8")


def seed_interactions():
    rows = [
        {"user": "Avery", "item": "AI Strategy", "rating": 1},
        {"user": "Avery", "item": "Prompt Library", "rating": 1},
        {"user": "Avery", "item": "ML Ops", "rating": 1},
        {"user": "Jordan", "item": "Design Systems", "rating": 1},
        {"user": "Jordan", "item": "AI Strategy", "rating": 1},
        {"user": "Casey", "item": "ML Ops", "rating": 1},
        {"user": "Casey", "item": "Data Pipelines", "rating": 1},
        {"user": "Taylor", "item": "Growth Analytics", "rating": 1},
        {"user": "Taylor", "item": "AI Strategy", "rating": 1},
    ]
    save_interactions(rows)
    return rows


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(WEB_DIR), **kwargs)

    def log_message(self, format, *args):
        return

    def _send_json(self, payload, status=HTTPStatus.OK):
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == "/api/users":
            users, items, matrix = build_matrices(load_interactions())
            self._send_json({"users": users})
            return
        if parsed.path == "/api/items":
            users, items, matrix = build_matrices(load_interactions())
            self._send_json({"items": items})
            return
        if parsed.path == "/api/recommend":
            query = parse_qs(parsed.query)
            user_id = query.get("user_id", [""])[0]
            users, items, matrix = build_matrices(load_interactions())
            if user_id not in users:
                self._send_json({"error": "Unknown user"}, HTTPStatus.BAD_REQUEST)
                return
            similarity = build_item_similarity(matrix)
            user_idx = users.index(user_id)
            ranked = recommend(user_idx, matrix, similarity, top_k=3)
            results = [{"item": items[idx], "score": round(score, 3)} for idx, score in ranked]
            self._send_json({"results": results})
            return
        if parsed.path.startswith("/api/"):
            self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        super().do_GET()

    def do_POST(self):
        if self.path == "/api/seed":
            rows = seed_interactions()
            self._send_json({"count": len(rows)})
            return
        self._send_json({"error": "Not found"}, HTTPStatus.NOT_FOUND)


def run(host="127.0.0.1", port=5173):
    server = ThreadingHTTPServer((host, port), Handler)
    print(f"RecoFoundry running at http://{host}:{port}")
    server.serve_forever()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Run RecoFoundry")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=5173)
    args = parser.parse_args()

    run(host=args.host, port=args.port)
