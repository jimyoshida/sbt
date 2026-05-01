#!/usr/bin/env python3
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Optional

import typer

app = typer.Typer()


# tutorial as-is
@app.command()
def goodbye(name: str, formal: bool = False):
    if formal:
        typer.echo(f"Goodbye Ms. {name}. Have a good day.")
    else:
        typer.echo(f"Bye {name}!")


@app.command()
def sync(srcpath: str, dstpath: str, full: bool = False):
    src = Path(srcpath)
    dst = Path(dstpath)
    snapshot = dst / f"backup-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

    prior = None
    if not full:
        candidates = sorted(dst.glob("backup-*"))
        if candidates:
            prior = candidates[-1]

    cmd = ["rsync", "-avh"]
    if prior:
        typer.echo(f"🌙 Execute Incremental Backup on {prior.name}")
        cmd.append(f"--link-dest={prior}")
    else:
        typer.echo("🌕 Execute Full Backup")

    cmd += [str(src) + "/", str(snapshot)]
    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise typer.Exit(1)


@app.command()
def archive(srcpath: str, volname: str, pubname: Optional[str] = None):
    cmd = ["mkisofs", "-J", "-r", "-U", "-D", "-V", volname]
    if pubname:
        cmd += ["-P", pubname]
    cmd += ["-o", f"{volname}.iso", srcpath]

    result = subprocess.run(cmd)
    if result.returncode != 0:
        raise typer.Exit(1)


if __name__ == "__main__":
    app()
