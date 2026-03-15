#!/usr/bin/env python3
import argparse
import json
import os
import sys
from tqdm import tqdm

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.providers.uhc.scraper import scrape_policy_urls
from app.providers.uhc.downloader import download_pdfs
from app.providers.uhc.parser import parse_pdf
from app.providers.uhc.chunker import create_chunks
from app.config import PROVIDER_REGISTRY

CHECKPOINT_FILE = "data/ingestion_checkpoint.json"

def load_checkpoint():
    if os.path.exists(CHECKPOINT_FILE):
        with open(CHECKPOINT_FILE) as f:
            return json.load(f)
    return {"processed": []}

def save_checkpoint(checkpoint):
    os.makedirs(os.path.dirname(CHECKPOINT_FILE), exist_ok=True)
    with open(CHECKPOINT_FILE, "w") as f:
        json.dump(checkpoint, f)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--provider", default="uhc")
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()

    cfg = PROVIDER_REGISTRY.get(args.provider)
    if not cfg:
        print(f"Unknown provider: {args.provider}")
        sys.exit(1)

    print(f"Scraping {args.provider} policy URLs...")
    policies = scrape_policy_urls()

    if args.limit:
        policies = policies[:args.limit]

    print(f"Found {len(policies)} policies. Downloading PDFs...")
    pdf_paths = download_pdfs(policies)

    checkpoint = {} if args.refresh else load_checkpoint()
    processed = set(checkpoint.get("processed", []))

    print("Parsing and chunking PDFs...")
    all_chunks = []
    policy_map = {os.path.basename(p["url"]): p for p in policies}

    for pdf_path in tqdm(pdf_paths):
        if not args.refresh and pdf_path in processed:
            continue
        filename = os.path.basename(pdf_path)
        policy_info = policy_map.get(filename, {})
        source_url = policy_info.get("url", "")

        try:
            parsed = parse_pdf(pdf_path)
            if parsed.get("ocr_required"):
                print(f"  OCR required (skipping): {filename}")
                continue
            chunks = create_chunks(parsed, source_url=source_url, provider=args.provider)
            all_chunks.extend(chunks)
            processed.add(pdf_path)
            save_checkpoint({"processed": list(processed)})
        except Exception as e:
            print(f"  Error processing {filename}: {e}")

    print(f"\nTotal chunks: {len(all_chunks)}")
    print("Pushing to Qdrant...")

    from ingestion.push_to_qdrant import push_chunks
    push_chunks(all_chunks, collection_name=cfg["collection_name"])

    print("Done!")

if __name__ == "__main__":
    main()
