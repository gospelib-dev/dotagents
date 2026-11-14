# Running a root installer without sudo (user + mount namespace)

Goal: run `install.sh` for real (downloads, `install`, `visudo`, file moves) against
copies of `/etc`, `/usr/local`, `/var`, so the host is untouched.

```bash
unshare -r --mount bash harness.sh <repo>
```

The harness, run as namespace root:

```bash
T=$(mktemp -d); mkdir -p $T/{etc,usrlocal,var/lib,var/log}
cp -a /etc/. $T/etc/ 2>/dev/null || true          # unreadable files are skipped
cp -a /usr/local/. $T/usrlocal/ 2>/dev/null || true
: >$T/etc/shadow; : >$T/etc/gshadow
printf 'root ALL=(ALL:ALL) ALL\n@includedir /etc/sudoers.d\n' >$T/etc/sudoers; chmod 0440 $T/etc/sudoers
echo 'svc:x:0:0::/var/lib/svc:/usr/sbin/nologin' >>$T/etc/passwd; echo 'svc:x:0:' >>$T/etc/group
mount --bind $T/etc /etc; mount --bind $T/usrlocal /usr/local
mount --bind $T/var/lib /var/lib; mount --bind $T/var/log /var/log
# create fake secret files, run install.sh twice (second run with no args = idempotence),
# then ls -l the results, cat the sudoers file, confirm the sources are gone, cmp the runner
```

Why each step:
- `/etc/sudoers` and `/etc/shadow` are unreadable to a normal user, so the copy lacks them. Write a minimal sudoers so `visudo -c` has something to parse, and add empty shadow files for useradd.
- `unshare -r` maps only uid 0, and chown to any other uid fails. Pre-seed the service user as uid 0. That leaves `useradd` and cross-user ownership untested, so say so in the PR. `--map-auto` would map a full range but needs `newuidmap` (the `uidmap` package).
- `cmd | head -1` under `set -o pipefail` can exit the harness via SIGPIPE. Use `sed -n 1p`.
