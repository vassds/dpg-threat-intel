import urllib.request
import os

SOURCES = [
    "https://raw.githubusercontent.com/StevenBlack/hosts/master/alternates/tracking-only/hosts",
    "https://pgl.yoyo.org/adservers/serverlist.php?hostformat=nohtml",
    "https://v.firebog.net/hosts/Easyprivacy.txt",
    "https://v.firebog.net/hosts/Prigent-Ads.txt"
]

master_list = set()
print("[*] Starting Threat Intel Aggregation...")

for url in SOURCES:
    print(f"[-] Fetching from {url}...")
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=10) as response:
            lines = response.read().decode('utf-8').splitlines()
            for line in lines:
                clean_line = line.strip()
                if not clean_line or clean_line.startswith('#'):
                    continue
                if clean_line.startswith('0.0.0.0 '):
                    clean_line = clean_line.replace('0.0.0.0 ', '')
                elif clean_line.startswith('127.0.0.1 '):
                    clean_line = clean_line.replace('127.0.0.1 ', '')
                master_list.add(clean_line)
    except Exception as e:
        print(f"[!] Failed to fetch {url}: {e}")

output_file = "master_blocklist.txt"
with open(output_file, "w") as f:
    for domain in sorted(master_list):
        f.write(f"{domain}\n")

print(f"[*] Success! {len(master_list)} unique domains saved to {output_file}")
