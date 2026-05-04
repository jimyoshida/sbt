# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

`sbt` (Simple Backup Tool) is a Python 3 CLI utility that wraps `rsync` and `mkisofs` to provide backup operations. It is distributed as a Debian `.deb` package.

## Build Commands

```bash
make          # Build the .deb package → out/sbt_1.0.0-1_all.deb
make install  # Install via dpkg
make uninstall # Remove installed package
make clean    # Remove out/ and tmp/ build artifacts
```

There are no automated tests; testing is done by running the CLI manually.

## Architecture

The entire application lives in a single file: `sbt.py` (~60 lines). It uses [Typer](https://typer.tiangolo.com/) to expose two commands:

- **`sbt sync <srcdir> <dstdir>`** — incremental/full directory backups using `rsync`. Creates timestamped snapshot directories (`backup-YYYYMMDD-HHMMSS`). Supports hardlink-based incremental backups via rsync's `--link-dest`. Pass `--full` to force a full backup.
- **`sbt iso <srcdir> <dstdir>`** — creates ISO 9660 images from a directory using `mkisofs` (provided by `genisoimage`). Outputs `<VOLNAME>.iso` in `<dstdir>` (created if absent), with Joliet and Rock Ridge extensions for cross-platform compatibility. `--volname` defaults to the source directory name uppercased; must be uppercase letters, digits, underscores, and hyphens only, max 32 characters. `--pubname` sets the publisher string in the image header.

External tools are invoked via `subprocess.run()`. Errors result in `typer.Exit(1)`.

## Packaging

- `DEBIAN/control` — Debian package metadata (version, dependencies: `genisoimage`, `rsync`, `python3-typer`)
- `build-deb.sh` — shell script that assembles the package structure in `tmp/` and runs `dpkg-deb`
- `sbt.1` — Unix man page documenting all commands, arguments, and usage examples
