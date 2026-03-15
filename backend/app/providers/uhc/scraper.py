import json
import time
import os
import requests
from bs4 import BeautifulSoup
from typing import List, Dict

POLICY_INDEX_URL = "https://www.uhcprovider.com/en/policies-protocols/commercial-policies/commercial-medical-drug-policies.html"
CACHE_FILE = "data/uhc_policy_urls.json"

def scrape_policy_urls(cache_file: str = CACHE_FILE) -> List[Dict[str, str]]:
    if os.path.exists(cache_file):
        with open(cache_file) as f:
            return json.load(f)

    headers = {"User-Agent": "Mozilla/5.0 (compatible; PolicyBot/1.0)"}
    resp = requests.get(POLICY_INDEX_URL, headers=headers, timeout=30)
    resp.raise_for_status()
    time.sleep(0.5)

    soup = BeautifulSoup(resp.text, "html.parser")
    policies = []
    seen = set()

    for a in soup.find_all("a", href=True):
        href = a["href"]
        if "/content/dam/provider/docs/public/policies/comm-medical-drug/" in href and href.endswith(".pdf"):
            if "update" in href.lower() or "bulletin" in href.lower():
                continue
            if href in seen:
                continue
            seen.add(href)
            url = href if href.startswith("http") else f"https://www.uhcprovider.com{href}"
            name = a.get_text(strip=True) or os.path.basename(href).replace(".pdf", "").replace("-", " ").title()
            policies.append({"policy_name": name, "url": url})

    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, "w") as f:
        json.dump(policies, f, indent=2)

    return policies
