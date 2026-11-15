"""Job hunt tracker: serves index.html and a JSON API over a single jobs.json file."""

import argparse
import json
import os
import shutil
import threading
from datetime import datetime
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

HERE = Path(__file__).resolve().parent
DATA_DIR = Path(os.environ.get("DATA_DIR", Path.home() / "data" / "job-hunt"))
BACKUP_DIR = Path(os.environ.get("BACKUP_DIR", HERE.parent / "backups"))


class Store:
    def __init__(self, path: Path):
        self.path = path
        self.lock = threading.Lock()
        path.parent.mkdir(parents=True, exist_ok=True)
        self.jobs = json.loads(path.read_text()) if path.exists() else {}

    def _save(self):
        # Write-then-rename so a crash or a backup copy never sees a half-written file.
        tmp = self.path.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.jobs, ensure_ascii=False, indent=1))
        os.replace(tmp, self.path)

    def list(self):
        with self.lock:
            return [{"id": k, **v} for k, v in self.jobs.items()]

    def add(self, docs):
        """Insert docs whose id is new; existing jobs keep the user's status and notes."""
        with self.lock:
            added = []
            for d in docs:
                i = d["id"]
                if i not in self.jobs:
                    self.jobs[i] = {k: v for k, v in d.items() if k != "id"}
                    added.append(i)
            if added:
                self._save()
            return added

    def patch(self, job_id, fields):
        with self.lock:
            job = self.jobs[job_id]
            job.update({k: v for k, v in fields.items() if k != "id"})
            self._save()
            return {"id": job_id, **job}


def backup(src: Path = None, dest_dir: Path = None) -> Path:
    src = src or DATA_DIR / "jobs.json"
    dest_dir = dest_dir or BACKUP_DIR
    dest_dir.mkdir(parents=True, exist_ok=True)
    # shortcut: backups are never pruned; at ~100 KB each that is fine for a job hunt.
    dest = dest_dir / f"jobs-{datetime.now():%Y-%m-%d-%H%M%S}.json"
    shutil.copyfile(src, dest)
    return dest


def make_handler(store: Store):
    page = HERE / "index.html"

    class Handler(BaseHTTPRequestHandler):
        def _send(self, code, body, ctype="application/json"):
            data = body if isinstance(body, bytes) else json.dumps(body, ensure_ascii=False).encode()
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(data)))
            self.send_header("Cache-Control", "no-store")
            self.end_headers()
            self.wfile.write(data)

        def _body(self):
            return json.loads(self.rfile.read(int(self.headers.get("Content-Length", 0))) or b"null")

        def do_GET(self):
            if self.path in ("/", "/index.html"):
                self._send(200, page.read_bytes(), "text/html; charset=utf-8")
            elif self.path == "/api/jobs":
                self._send(200, store.list())
            else:
                self._send(404, {"error": "not found"})

        def do_POST(self):
            if self.path != "/api/jobs":
                return self._send(404, {"error": "not found"})
            try:
                docs = self._body()
                if not isinstance(docs, list) or not all(isinstance(d, dict) and isinstance(d.get("id"), str) and d["id"] for d in docs):
                    raise ValueError
            except ValueError:
                return self._send(400, {"error": "body must be a JSON array of objects with a string id"})
            self._send(200, {"added": store.add(docs)})

        def do_PATCH(self):
            prefix = "/api/jobs/"
            if not self.path.startswith(prefix):
                return self._send(404, {"error": "not found"})
            try:
                fields = self._body()
                if not isinstance(fields, dict):
                    raise ValueError
            except ValueError:
                return self._send(400, {"error": "body must be a JSON object"})
            try:
                self._send(200, store.patch(self.path[len(prefix):], fields))
            except KeyError:
                self._send(404, {"error": "no such job"})

        def log_message(self, *args):
            pass

    return Handler


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("command", nargs="?", default="serve", choices=["serve", "backup"])
    p.add_argument("--host", default="127.0.0.1")
    p.add_argument("--port", type=int, default=20210)
    a = p.parse_args()
    if a.command == "backup":
        print(backup())
        return
    store = Store(DATA_DIR / "jobs.json")
    print(f"Serving {len(store.jobs)} jobs from {store.path} on http://{a.host}:{a.port}", flush=True)
    ThreadingHTTPServer((a.host, a.port), make_handler(store)).serve_forever()


if __name__ == "__main__":
    main()
