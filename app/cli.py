import argparse
from app import main as run_main
from app.list_skills import list_skills
from app.delete_skill import delete_site


def create_parser():
    parser = argparse.ArgumentParser(
        description="Skillmaker CLI - Crawl documentation sites and save as markdown",
        prog="skillmaker"
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # CRAWL command (default behavior)
    crawl_parser = subparsers.add_parser(
        "crawl",
        help="Crawl a documentation site and save as markdown"
    )
    crawl_parser.add_argument(
        "url",
        type=str,
        help="Documentation URL to crawl and save"
    )
    # crawl_parser.add_argument(
    #     "--clean-with-llm",
    #     action="store_true",
    #     help="Use Claude API to remove duplicates and artifacts from concatenated markdown"
    # )
    # crawl_parser.add_argument(
    #     "--use-batch",
    #     action="store_true",
    #     help="Use Claude batch processing API for 50%% cost savings (requires --clean-with-llm)"
    # )
    # crawl_parser.add_argument(
    #     "--clean-pages",
    #     action="store_true",
    #     help="Apply intermediate page-level cleaning with LLM-generated functions before concatenation"
    # )

    # LIST command
    list_parser = subparsers.add_parser(
        "list",
        help="List all crawled skills with statistics"
    )

    # DELETE command
    delete_parser = subparsers.add_parser(
        "delete",
        help="Delete all traces of a crawled site"
    )
    delete_parser.add_argument(
        "url",
        type=str,
        help="URL of the site to delete"
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    # If no command specified, show help
    if not args.command:
        parser.print_help()
        return

    # Route to appropriate command
    if args.command == "list":
        list_skills()
    elif args.command == "delete":
        delete_site(args.url)
    elif args.command == "crawl":
        run_main(
            args.url,
            use_llm_cleaning=args.clean_with_llm,
            use_batch=args.use_batch,
            use_page_cleaning=args.clean_pages
        )


if __name__ == "__main__":
    main()
