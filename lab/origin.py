#!/usr/bin/env python3
"""TCP and UDS origin servers for the ATS ESI recv-port leftover lab."""

from __future__ import annotations

import os
import threading
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from socketserver import UnixStreamServer
from typing import Any

WITNESS = os.environ.get("WITNESS", "ATS-ESI-UNIX-RECVPORT-WITNESS")
ROLE = os.environ.get("ORIGIN_ROLE", "tcp")
LISTEN_HOST = os.environ.get("LISTEN_HOST", "0.0.0.0")
LISTEN_PORT = int(os.environ.get("LISTEN_PORT", "8080"))
UDS_PATH = os.environ.get("UDS_PATH", "/uds/origin.sock")
TCP_BODY = "TCP-ORIGIN-OK"
ESI_PAGE = (
    "<html><body>ESI\n"
    '<esi:include src="http://www.example.com/secret"/>\n'
    "</body></html>\n"
)


def log(msg: str) -> None:
    print(msg, flush=True)


class OriginHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: Any) -> None:
        peer = self._peer_label()
        log(f"{ROLE} {peer} {fmt % args}")

    def _peer_label(self) -> str:
        addr = self.client_address
        if isinstance(addr, tuple):
            return f"tcp={addr[0]}:{addr[1]}"
        if addr:
            return f"uds={addr}"
        return "uds=anon"

    def _send(self, status: int, body: str, extra: dict[str, str] | None = None) -> None:
        payload = body.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("Connection", "close")
        self.send_header("X-Origin-Role", ROLE)
        self.send_header("X-Origin-Peer", self._peer_label())
        if extra:
            for key, value in extra.items():
                self.send_header(key, value)
        self.end_headers()
        if self.command != "HEAD":
            self.wfile.write(payload)

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/health":
            self._send(200, "ok\n")
            return
        if ROLE == "tcp":
            self._handle_tcp(path)
            return
        self._handle_uds(path)

    def do_HEAD(self) -> None:
        self.do_GET()

    def _handle_tcp(self, path: str) -> None:
        if path == "/page":
            self._send(200, ESI_PAGE, extra={"X-Esi": "1"})
            return
        if path in {"/secret", "/tcp-secret"}:
            self._send(200, f"{TCP_BODY}\n")
            return
        self._send(404, "tcp-miss\n")

    def _handle_uds(self, path: str) -> None:
        if path == "/secret":
            self._send(200, f"{WITNESS}\n", extra={"X-Esi-Unix-Origin": "1"})
            return
        if path == "/page":
            self._send(200, "UDS-PAGE\n")
            return
        self._send(404, "uds-miss\n")


class UdsHTTPServer(UnixStreamServer):
    daemon_threads = True
    allow_reuse_address = True

    def get_request(self) -> tuple[socket.socket, str]:
        conn, _ = super().get_request()
        return conn, "unix"


def _bind_tcp() -> ThreadingHTTPServer:
    httpd = ThreadingHTTPServer((LISTEN_HOST, LISTEN_PORT), OriginHandler)
    httpd.daemon_threads = True
    return httpd


def _bind_uds() -> UdsHTTPServer:
    parent = os.path.dirname(UDS_PATH)
    if parent:
        os.makedirs(parent, exist_ok=True)
    try:
        os.unlink(UDS_PATH)
    except FileNotFoundError:
        pass
    httpd = UdsHTTPServer(UDS_PATH, OriginHandler)
    os.chmod(UDS_PATH, 0o666)
    return httpd


def main() -> int:
    tcp = _bind_tcp()
    log(f"origin-role={ROLE} tcp={LISTEN_HOST}:{LISTEN_PORT}")
    if ROLE == "uds":
        uds = _bind_uds()
        log(f"origin-role={ROLE} uds={UDS_PATH}")
        threading.Thread(target=uds.serve_forever, name="uds", daemon=True).start()
    try:
        tcp.serve_forever()
    except KeyboardInterrupt:
        pass
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
