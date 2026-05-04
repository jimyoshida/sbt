# sbt (simple backup tool)

See also `DEBIAN/control`.

## Build

To build the package, you will need:

* Ubuntu 24.04+
* GNU Make 4.3+
* dpkg-deb (included in the `dpkg` package)

Run `make` to generate the deb package.

## Install

Run `sudo make install` to install the package.

## Using Windows drives from WSL

Windows drives are mounted at `/mnt/<letter>` (e.g. `/mnt/d`, `/mnt/e`). C: is auto-mounted by WSL; other drives may need to be mounted manually or added to `/etc/fstab`:

```bash
# Mount a drive for the current session
sudo mkdir -p /mnt/e && sudo mount -t drvfs E: /mnt/e

# Make it persist across WSL restarts — add to /etc/fstab
echo 'E: /mnt/e drvfs defaults 0 0' | sudo tee -a /etc/fstab
```

If a drive shows "No such device" despite appearing in `mount`, remount it:

```bash
sudo umount /mnt/d && sudo mount -t drvfs D: /mnt/d
```
