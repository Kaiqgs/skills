import os
import app.folder_structure as folder_structure
import random
import logging
from typing import List

max_tokens = 200_000

def sample_pages_for_analysis(page_dir, target_tokens = 100_000) -> str:

    page_paths = folder_structure.get_all_pages(page_dir)

    page_paths: List[str]

    # Step 1: Read all pages and calculate total length
    page_contents = []
    total_chars = 0

    for page_path in page_paths:
        if not os.path.exists(page_path):
            logging.warning(f"  ⚠ Page not found: {page_path}")
            continue

        with open(page_path, "r", encoding="utf-8") as f:
            content = f.read()
            page_contents.append({
                "path": page_path,
                "content": content,
                "length": len(content)
            })
            total_chars += len(content)

    if total_chars == 0:
        logging.warning("  ⚠ No content found in pages")
        return ""

    # 1_token = 4_chars
    # 4_token = 16_chars
    token_goal = min(max_tokens, total_chars // 4, target_tokens)
    sample_percentage = token_goal / total_chars

    logging.info(f"  → Sampling {len(page_paths)} page(s) at {sample_percentage*100:.1f}% rate...")

    # Step 2: Calculate target sample size
    target_sample_chars = int(total_chars * sample_percentage)
    logging.info(f"  → Total content: {total_chars:,} chars, target sample: {target_sample_chars:,} chars")

    # Step 3: Sample each page proportionally
    sampled_content = []
    sampled_content.append(f"# DOCUMENTATION SAMPLES ({len(page_contents)} pages)\n")
    sampled_content.append(f"# Total content: {total_chars:,} chars, Sample budget: {target_sample_chars:,} chars\n")
    sampled_content.append("=" * 80 + "\n\n")

    for page_data in page_contents:
        page_path = page_data["path"]
        content = page_data["content"]
        page_length = page_data["length"]

        # Calculate this page's sample budget (proportional to its size)
        page_sample_budget = int((page_length / total_chars) * target_sample_chars)

        if page_sample_budget == 0:
            continue  # Skip very small pages

        # Split budget: 40% head, 40% tail, 20% random middle
        head_budget = int(page_sample_budget * 0.4)
        tail_budget = int(page_sample_budget * 0.4)
        middle_budget = page_sample_budget - head_budget - tail_budget

        # Sample head
        head_sample = content[:head_budget]

        # Sample tail
        tail_sample = content[-tail_budget:] if tail_budget > 0 else ""

        # Sample random middle
        middle_start = head_budget
        middle_end = max(middle_start, page_length - tail_budget)
        middle_sample = ""

        if middle_budget > 0 and middle_end > middle_start:
            # Extract a continuous chunk from the middle region
            available_length = middle_end - middle_start
            if available_length > middle_budget:
                # Random starting point in the middle region
                random_start = random.randint(middle_start, middle_end - middle_budget)
                middle_sample = content[random_start:random_start + middle_budget]
            else:
                # Take entire middle region if it's smaller than budget
                middle_sample = content[middle_start:middle_end]

        # Add to sampled content with clear separators
        page_name = os.path.basename(page_path)
        sampled_content.append(f"\n{'='*80}\n")
        sampled_content.append(f"## PAGE: {page_name}\n")
        sampled_content.append(f"## Length: {page_length:,} chars | Sample budget: {page_sample_budget:,} chars\n")
        sampled_content.append(f"{'='*80}\n\n")

        sampled_content.append(f"### HEAD SAMPLE ({len(head_sample)} chars):\n")
        sampled_content.append(head_sample)
        sampled_content.append(f"\n\n[... middle content omitted ...]\n\n")

        if middle_sample:
            sampled_content.append(f"### RANDOM MIDDLE SAMPLE ({len(middle_sample)} chars):\n")
            sampled_content.append(middle_sample)
            sampled_content.append(f"\n\n[... content omitted ...]\n\n")

        sampled_content.append(f"### TAIL SAMPLE ({len(tail_sample)} chars):\n")
        sampled_content.append(tail_sample)
        sampled_content.append("\n\n")

    result = "".join(sampled_content)
    logging.info(f"  ✓ Generated {len(result):,} char sample from {len(page_contents)} page(s)")

    return result
