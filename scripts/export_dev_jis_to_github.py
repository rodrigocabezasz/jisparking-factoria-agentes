#!/usr/bin/env python3
"""
Exporta el sandbox generado por factory-runner:
  /workspaces/dev-jis-work/<request_id>/{src,tests}
y lo copia a un repo GitHub (creando una rama).

Se asume que el repo destino YA EXISTE (puede estar vacío en GitHub; el clon
sin shallow se usa como respaldo si `--depth=1` falla).

Variables recomendadas:
  - GITHUB_TOKEN: token con permisos para push al repo destino
"""

from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def run(cmd: list[str], cwd: Path | None = None) -> None:
    subprocess.run(cmd, cwd=str(cwd) if cwd else None, check=True)


def clone_dest_repo(clone_url: str, dest: Path) -> None:
    """
    GitHub: `git clone --depth=1` falla en repos vacíos (no hay commits que fetch).
    En ese caso reintentamos sin --depth.
    """
    try:
        run(["git", "clone", "--depth=1", clone_url, dest])
    except subprocess.CalledProcessError:
        run(["git", "clone", clone_url, dest])


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--request-id", "-r", required=True)
    ap.add_argument("--src-base", default="/workspaces/dev-jis-work")
    ap.add_argument("--target-repo", "-R", required=True, help="owner/repo")
    ap.add_argument("--token", default=os.getenv("GITHUB_TOKEN", ""), help="GITHUB_TOKEN (o --token)")
    ap.add_argument("--branch", default=None, help="rama a crear (default: factoria/<request_id>)")
    ap.add_argument(
        "--commit-message",
        default=None,
        help="default: 'Factory Dev_JIS export <request_id>'",
    )
    args = ap.parse_args()

    token = (args.token or "").strip()
    if not token:
        print("ERROR: falta GITHUB_TOKEN (o pasa --token)", file=sys.stderr)
        return 2

    request_id = args.request_id.strip()
    src_dir = Path(args.src_base) / request_id
    if not src_dir.exists():
        print(f"ERROR: sandbox no existe: {src_dir}", file=sys.stderr)
        return 3

    for sub in ["src", "tests"]:
        if not (src_dir / sub).exists():
            print(f"ERROR: faltan archivos en {src_dir}/{sub}", file=sys.stderr)
            return 4

    branch = args.branch or f"factoria/{request_id}"
    commit_message = args.commit_message or f"Factory Dev_JIS export {request_id}"

    owner_repo = args.target_repo.strip()
    if "/" not in owner_repo:
        print("ERROR: --target-repo debe ser owner/repo", file=sys.stderr)
        return 5

    # GitHub HTTPS con token en URL (operativo para tareas ad-hoc).
    # Nota: evita imprimir el token.
    clone_url = f"https://x-access-token:{token}@github.com/{owner_repo}.git"

    with tempfile.TemporaryDirectory(prefix=f"export-{request_id}-") as td:
        work = Path(td)
        clone_dest_repo(clone_url, work / "repo")
        repo = work / "repo"

        # Trabajamos en la rama destino.
        run(["git", "checkout", "-B", branch], cwd=repo)

        # Reemplazamos carpetas src/tests del repo.
        for sub in ["src", "tests"]:
            dst = repo / sub
            if dst.exists():
                shutil.rmtree(dst)
            shutil.copytree(src_dir / sub, dst)

        run(["git", "add", "-A"], cwd=repo)
        # commit puede fallar si no hay cambios respecto a la rama base
        try:
            run(["git", "commit", "-m", commit_message], cwd=repo)
        except subprocess.CalledProcessError:
            print("INFO: no hubo cambios para commitear (commit saltado).", file=sys.stderr)

        run(["git", "push", "-u", "origin", branch], cwd=repo)

    print(f"OK: export listo. Rama: {branch} Repo: {owner_repo}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

