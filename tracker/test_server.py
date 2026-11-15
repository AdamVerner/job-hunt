import json
import tempfile
import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from pathlib import Path

import server


def call(base, method, path, body=None):
    req = urllib.request.Request(base + path, method=method, data=None if body is None else json.dumps(body).encode(),
                                 headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req) as r:
            return r.status, json.loads(r.read())
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read())


class ScanAndTrackFlow(unittest.TestCase):
    def test_scan_then_user_edits_then_rescan(self):
        tmp = Path(tempfile.mkdtemp())
        store = server.Store(tmp / "jobs.json")
        httpd = ThreadingHTTPServer(("127.0.0.1", 0), server.make_handler(store))
        threading.Thread(target=httpd.serve_forever, daemon=True).start()
        base = f"http://127.0.0.1:{httpd.server_port}"

        # first scan adds two jobs
        status, res = call(base, "POST", "/api/jobs", [{"id": "a--x", "status": "new", "score": 3}, {"id": "b--y", "status": "new"}])
        self.assertEqual((status, res["added"]), (200, ["a--x", "b--y"]))

        # user stars one and adds a note
        status, job = call(base, "PATCH", "/api/jobs/a--x", {"status": "interested", "notes": [{"date": "2026-11-15", "text": "call"}]})
        self.assertEqual((status, job["status"], job["score"]), (200, "interested", 3))

        # rescan finds the same job again: the user's edits survive
        _, res = call(base, "POST", "/api/jobs", [{"id": "a--x", "status": "new", "score": 5}, {"id": "c--z"}])
        self.assertEqual(res["added"], ["c--z"])
        jobs = {j["id"]: j for j in call(base, "GET", "/api/jobs")[1]}
        self.assertEqual((jobs["a--x"]["status"], jobs["a--x"]["score"], len(jobs)), ("interested", 3, 3))

        # data survives a restart, and a backup is a full copy
        self.assertEqual(server.Store(tmp / "jobs.json").jobs["a--x"]["notes"][0]["text"], "call")
        copy = server.backup(tmp / "jobs.json", tmp / "backups")
        self.assertEqual(len(json.loads(copy.read_text())), 3)

        # bad input is refused
        self.assertEqual(call(base, "POST", "/api/jobs", [{"no": "id"}])[0], 400)
        self.assertEqual(call(base, "PATCH", "/api/jobs/missing", {"status": "new"})[0], 404)
        httpd.shutdown()


if __name__ == "__main__":
    unittest.main()
