import os
import time
import logging
import requests
from typing import List, Dict

logger = logging.getLogger(__name__)

def download_pdfs(policies: List[Dict[str, str]], dest_dir: str = "data/pdfs/uhc", fail_log: str = "data/failed_downloads.log") -> List[str]:
    os.makedirs(dest_dir, exist_ok=True)
    downloaded = []

    for policy in policies:
        url = policy["url"]
        filename = os.path.basename(url)
        dest_path = os.path.join(dest_dir, filename)

        if os.path.exists(dest_path):
            downloaded.append(dest_path)
            continue

        for attempt in range(3):
            try:
                time.sleep(1)
                headers = {"User-Agent": "Mozilla/5.0 (compatible; PolicyBot/1.0)"}
                resp = requests.get(url, headers=headers, timeout=60)
                resp.raise_for_status()
                with open(dest_path, "wb") as f:
                    f.write(resp.content)
                downloaded.append(dest_path)
                break
            except Exception as e:
                if attempt == 2:
                    logger.error(f"Failed to download {url}: {e}")
                    with open(fail_log, "a") as f:
                        f.write(f"{url}\t{e}\n")
                else:
                    time.sleep(2 ** attempt)

    return downloaded
