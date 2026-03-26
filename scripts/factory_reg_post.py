#!/usr/bin/env python3
"""
Registro /reg hacia jis-intake sin depender de curl ni puertos inventados por el LLM.
Uso:
  printf '%s' 'texto del requerimiento' | python3 factory_reg_post.py
  echo 'texto' | python3 factory_reg_post.py
  python3 factory_reg_post.py --file /ruta/requerimiento.txt
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

INTAKE = "http://127.0.0.1:8089/telegram/reg"


def main() -> int:
    parser = argparse.ArgumentParser(description="POST /telegram/reg al intake JISLAB")
    parser.add_argument(
        "--file",
        "-f",
        metavar="PATH",
        help="UTF-8: leer el requerimiento desde archivo (alternativa a stdin)",
    )
    args = parser.parse_args()

    if args.file:
        try:
            text = Path(args.file).read_text(encoding="utf-8").strip()
        except OSError as e:
            print(f"ERROR: no se pudo leer {args.file}: {e}", file=sys.stderr)
            return 2
    else:
        text = sys.stdin.read().strip()
    if not text:
        print(
            "ERROR: texto vacío; usá stdin, o --file RUTA.",
            file=sys.stderr,
        )
        return 2
    body = json.dumps({"text": text, "username": "openclaw-ui"}).encode("utf-8")
    req = urllib.request.Request(
        INTAKE,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=60) as resp:
            out = resp.read().decode("utf-8", errors="replace")
            sys.stdout.write(out)
            if not out.endswith("\n"):
                sys.stdout.write("\n")
    except urllib.error.HTTPError as e:
        sys.stdout.write(e.read().decode("utf-8", errors="replace"))
        return 1
    except OSError as e:
        print(f"ERROR: {e}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
