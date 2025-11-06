import argparse
import os
import shutil
from app import main as run_main
from app.url_to_name import url_to_name
from app.folder_structure import PAGES_DIR, SKILLS_DIR
from app.index import load_index, save_index


def delete_site(url: str):
    """Delete all traces of a crawled site from index, pages, and skills."""
    base_name = url_to_name(url)

    # Check what exists
    index = load_index()
    index_entry = index.get(url)
    pages_dir = os.path.join(PAGES_DIR, base_name)
    skill_file = os.path.join(SKILLS_DIR, f"{base_name}.md")

    items_to_delete = []

    if index_entry:
        items_to_delete.append(f"  - Index entry for: {url}")

    if os.path.exists(pages_dir):
        items_to_delete.append(f"  - Pages directory: {pages_dir}")

    if os.path.exists(skill_file):
        items_to_delete.append(f"  - Skill file: {skill_file}")

    if not items_to_delete:
        print(f"Nothing found for URL: {url}")
        return

    # Show what will be deleted
    print(f"The following will be deleted for '{base_name}':")
    for item in items_to_delete:
        print(item)

    # Ask for confirmation
    response = input("\nAre you sure you want to delete these items? (y/n): ").lower().strip()

    if response != 'y':
        print("Deletion cancelled.")
        return

    # Perform deletion
    if index_entry:
        del index[url]
        save_index(index)
        print(f"✓ Deleted index entry for: {url}")

    if os.path.exists(pages_dir):
        shutil.rmtree(pages_dir)
        print(f"✓ Deleted pages directory: {pages_dir}")

    if os.path.exists(skill_file):
        os.remove(skill_file)
        print(f"✓ Deleted skill file: {skill_file}")

    print("\nDeletion complete!")


def create_parser():
    parser = argparse.ArgumentParser(
        description="Skillmaker CLI - Crawl documentation sites and save as markdown",
        prog="skillmaker"
    )

    parser.add_argument(
        "url",
        type=str,
        default="https://hyperscript.org/docs/",
        help="Documentation URL to crawl and save"
    )

    parser.add_argument(
        "--clean-with-llm",
        action="store_true",
        help="Use Claude API to remove duplicates and artifacts from concatenated markdown"
    )

    parser.add_argument(
        "--use-batch",
        action="store_true",
        help="Use Claude batch processing API for 50%% cost savings (requires --clean-with-llm)"
    )

    parser.add_argument(
        "--delete",
        action="store_true",
        help="Delete all traces of a crawled site (index, pages, skill file)"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if args.delete:
        delete_site(args.url)
    else:
        run_main(args.url, use_llm_cleaning=args.clean_with_llm, use_batch=args.use_batch)


if __name__ == "__main__":
    main()
