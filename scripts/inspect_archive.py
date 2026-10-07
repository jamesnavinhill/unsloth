#!/usr/bin/env python3
"""
Archive Inspection & Triage Script
Reads directly from archive.zip without full disk extraction:
  1. Lists members, sizes, and compression ratios.
  2. Inspects schema, columns, and data formats per member.
  3. Samples first N rows to evaluate text quality, tokenization artifacts,
     language distribution, and relevance to target domains.
"""

import sys
import io
import csv
import zipfile
from pathlib import Path

# Increase CSV field size limit for large text blocks
csv.field_size_limit(2147483647)

# Fix stdout encoding
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

ZIP_PATH = Path(r"C:\Users\james\projects\labwork\datasets\human_written_text\archive.zip")

def inspect_zip():
    if not ZIP_PATH.exists():
        print(f"Error: {ZIP_PATH} does not exist.")
        return

    print("=" * 70)
    print("ARCHIVE INVENTORY & TRIAGE")
    print(f"File: {ZIP_PATH.name} ({ZIP_PATH.stat().st_size / 1e9:.2f} GB)")
    print("=" * 70)

    with zipfile.ZipFile(ZIP_PATH, "r") as zf:
        infolist = zf.infolist()
        total_uncompressed = sum(info.file_size for info in infolist)
        print(f"Total Members: {len(infolist)} | Total Uncompressed: {total_uncompressed / 1e9:.2f} GB\n")

        print(f"{'Member File':<25} {'Compressed':<12} {'Uncompressed':<14} {'Ratio':<8}")
        print("-" * 65)
        for info in infolist:
            comp_mb = info.compress_size / 1e6
            uncomp_mb = info.file_size / 1e6
            ratio = (info.compress_size / info.file_size * 100) if info.file_size > 0 else 0
            print(f"{info.filename:<25} {comp_mb:>8.1f} MB  {uncomp_mb:>10.1f} MB  {ratio:>6.1f}%")
        print("=" * 70)

        # Detailed Inspection per Member
        for info in infolist:
            if not info.filename.endswith(".csv"):
                continue
            
            print(f"\n>>> INSPECTING: {info.filename}")
            print("-" * 70)
            
            with zf.open(info.filename) as f:
                # Read first 1MB chunk to inspect headers and first few rows safely
                text_chunk = f.read(1024 * 1024).decode("utf-8", errors="replace")
                reader = csv.reader(io.StringIO(text_chunk))
                
                try:
                    headers = next(reader)
                    print(f"Columns ({len(headers)}): {headers}")
                except StopIteration:
                    print("Empty file")
                    continue
                
                rows_sampled = 0
                sample_lengths = []
                sample_snippets = []
                
                for row in reader:
                    if not row or rows_sampled >= 5:
                        break
                    # Identify text content
                    text = " ".join(row)
                    sample_lengths.append(len(text.split()))
                    sample_snippets.append(text[:250].replace("\n", " "))
                    rows_sampled += 1
                
                print(f"Sampled {rows_sampled} rows.")
                if sample_lengths:
                    print(f"Avg words per sample: ~{sum(sample_lengths)/len(sample_lengths):.0f} words")
                
                print("First 3 Row Previews:")
                for idx, snip in enumerate(sample_snippets[:3]):
                    print(f"  [{idx+1}] {snip}...")

if __name__ == "__main__":
    inspect_zip()
