"""Resumable, strictly sequential PhysioNet downloader (PhysioNet blocks parallel downloads).

  python py/download_physionet.py nstdb
  python py/download_physionet.py cebsdb b001 b002 ...                          (named records only)
  python py/download_physionet.py ltstdb --ext hea dat atr stc --dry-run         (print the total size, download nothing)
  python py/download_physionet.py ltstdb --ext hea dat atr stc --max-gb 8        (refuse if the preflight total is above 8 GB)
  python py/download_physionet.py ptb-xl --prefix records100 --ext hea dat --no-preflight \
        --extra ptbxl_database.csv scp_statements.csv

Round-2 extension of the original script: --ext (file types to fetch), --prefix (only records whose RECORDS path starts so),
--extra (extra top-level files), --dry-run / --max-gb / --no-preflight (size check before downloading), persistent HTTPS connection.
Files are written to <name>.part and renamed when the size matches Content-Length, so any file present without ".part" is complete:
re-running resumes an interrupted job.  Output: real_data/<short name>/.
Licences: ltstdb, edb, sddb, cudb, nsrdb, nstdb, cebsdb = Open Data Commons Attribution v1.0; ptb-xl = CC BY 4.0."""
import argparse, concurrent.futures as cf, http.client, os, sys, threading, time, urllib.parse
_tl = threading.local()
import wfdb.io.download as wd

OUT = {"nsrdb": "nsrdb", "nstdb": "nstdb", "cebsdb": "cebs", "ptb-xl": "ptbxl"}
HOST = "physionet.org"
HDR = {"User-Agent": "sentry-sim-research/1.0"}
_conns = {}


def conn(host):
    if host not in _conns:
        _conns[host] = http.client.HTTPSConnection(host, timeout=120)
    return _conns[host]


def request(method, path, retries=6, host=HOST):
    """GET/HEAD with a persistent connection per host; follows redirects, including to another host (PhysioNet serves some
    databases from physionet-open.s3.amazonaws.com)."""
    for k in range(retries):
        try:
            c = conn(host); c.request(method, path, headers=HDR); r = c.getresponse()
            if r.status in (301, 302, 303, 307, 308):
                loc = r.getheader("Location"); r.read()
                if loc.startswith("http"):
                    sp = urllib.parse.urlsplit(loc); host = sp.netloc; path = sp.path + ("?" + sp.query if sp.query else "")
                else:
                    path = loc
                continue
            return r
        except Exception:
            _conns.pop(host, None); time.sleep(2 * (k + 1))
    raise RuntimeError(f"giving up on {method} {path}")


def remote_size(path):
    r = request("HEAD", path); r.read()
    return int(r.getheader("Content-Length", -1)) if r.status == 200 else None


def fetch(path, dest):
    """returns (status, size): got / skip / absent"""
    if os.path.exists(dest):
        return "skip", os.path.getsize(dest)
    tmp = dest + ".part"
    for k in range(6):
        r = request("GET", path)
        if r.status == 404:
            r.read(); return "absent", 0
        if r.status != 200:
            r.read(); time.sleep(2 * (k + 1)); continue
        size = int(r.getheader("Content-Length", -1))
        try:
            with open(tmp, "wb") as f:
                while True:
                    ch = r.read(1 << 20)
                    if not ch: break
                    f.write(ch)
        except Exception:
            _conns.clear(); time.sleep(2 * (k + 1)); continue
        if size >= 0 and os.path.getsize(tmp) != size:
            time.sleep(2 * (k + 1)); continue
        os.replace(tmp, dest)
        return "got", os.path.getsize(dest)
    raise RuntimeError(f"giving up on {path}")


def s3_probe(base, sample):
    """If PhysioNet redirects this database to its S3 bucket, return (host, path-prefix); else None."""
    c = http.client.HTTPSConnection(HOST, timeout=60); c.request("HEAD", base + sample, headers=HDR); r = c.getresponse(); r.read()
    if r.status in (301, 302, 303, 307, 308) and "amazonaws.com" in (r.getheader("Location") or ""):
        sp = urllib.parse.urlsplit(r.getheader("Location")); return sp.netloc, sp.path[: len(sp.path) - len(sample)]
    return None


def fetch_s3(host, prefix, f, dest):
    """own persistent connection per thread (threading.local); S3 has no one-at-a-time rule"""
    if os.path.exists(dest): return "skip", os.path.getsize(dest)
    for k in range(6):
        try:
            c = _tl.__dict__.get("c")
            if c is None: c = _tl.c = http.client.HTTPSConnection(host, timeout=120)
            c.request("GET", prefix + f, headers=HDR); r = c.getresponse(); b = r.read()
            if r.status == 404: return "absent", 0
            if r.status == 200:
                tmp = dest + ".part"; open(tmp, "wb").write(b); os.replace(tmp, dest); return "got", len(b)
        except Exception:
            _tl.c = None; time.sleep(1 + k)
    raise RuntimeError(f"giving up on {f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("db"); ap.add_argument("records", nargs="*")
    ap.add_argument("--ext", nargs="+", default=["hea", "dat", "atr", "qrs"])
    ap.add_argument("--prefix", default=None); ap.add_argument("--extra", nargs="*", default=[])
    ap.add_argument("--dry-run", action="store_true"); ap.add_argument("--no-preflight", action="store_true")
    ap.add_argument("--max-gb", type=float, default=None); ap.add_argument("--threads", type=int, default=1, help="parallel connections, used only when PhysioNet serves the database from its S3 bucket")
    a = ap.parse_args()
    ver = wd.get_version(a.db)
    base = f"/files/{a.db}/{ver}/"
    out = os.path.join("real_data", OUT.get(a.db, a.db)); os.makedirs(out, exist_ok=True)
    if a.records:
        recs = a.records
    else:
        r = request("GET", base + "RECORDS"); txt = r.read().decode(errors="replace")
        if r.status != 200 or txt.lstrip().startswith("<"):        # some databases have no usable RECORDS file
            import wfdb; recs = wfdb.get_record_list(a.db)
        else:
            recs = [l.strip() for l in txt.splitlines() if l.strip()]
        if a.prefix: recs = [x for x in recs if x.startswith(a.prefix)]
    files = [(r_ + "." + e) for r_ in recs for e in a.ext] + list(a.extra)
    docs = ["README.txt", "info.txt", "RECORDS", "ANNOTATORS", "SHA256SUMS.txt", "LICENSE.txt", "00README"]
    if not a.no_preflight or a.dry_run:
        tot = 0; miss = 0
        for f in files:
            s = remote_size(base + f)
            if s is None: miss += 1
            else: tot += s
        print(f"preflight: {len(files)} files requested ({miss} do not exist), total {tot/1e9:.2f} GB for {a.db} {ver}", flush=True)
        if a.dry_run: return
        if a.max_gb is not None and tot / 1e9 > a.max_gb: sys.exit(f"refusing: {tot/1e9:.2f} GB is above --max-gb {a.max_gb}")
    for d in docs:
        st, _ = fetch(base + d, os.path.join(out, d)); print(f"{st:6s} {d}", flush=True)
    if a.threads > 1 and files:
        probe = s3_probe(base, files[0])
        if probe:
            host, prefix = probe; print(f"S3 mode: {host}{prefix}  threads={a.threads}", flush=True)
            for f in files: os.makedirs(os.path.dirname(os.path.join(out, f.replace("/", os.sep))), exist_ok=True)
            done = 0; total = 0
            with cf.ThreadPoolExecutor(a.threads) as ex:
                futs = [ex.submit(fetch_s3, host, prefix, f, os.path.join(out, f.replace("/", os.sep))) for f in files]
                for fu in cf.as_completed(futs):
                    st, sz = fu.result(); done += 1; total += sz
                    if done % 1000 == 0: print(f"  {done}/{len(files)} files, {total/1e6:.0f} MB", flush=True)
            print(f"done (S3): {a.db} {ver}, {len(files)} files, {total/1e6:.0f} MB in {out}"); return
    total = 0; n = 0
    for f in files:
        dest = os.path.join(out, f.replace("/", os.sep)); os.makedirs(os.path.dirname(dest), exist_ok=True)
        st, sz = fetch(base + f, dest)
        if st != "absent":
            total += sz; n += 1
            if st == "got" or n % 500 == 0: print(f"{st:6s} {f}  {sz/1e6:8.2f} MB   ({n}/{len(files)})", flush=True)
    print(f"done: {a.db} {ver}, {n} files, {total/1e6:.0f} MB on disk in {out}")


if __name__ == "__main__":
    main()
