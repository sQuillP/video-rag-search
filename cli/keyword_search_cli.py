import argparse
from lib import keyword_search

# Last left off: ch2 L1
def build_command():
    indices = keyword_search.InvertedIndex()
    indices.build()
    indices.save()
    print(f'First document for token "merida" = {indices.index.get('merida')}')

def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 1. Define search subparser
    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    # 2. Define build subparser with its own variable name
    build_parser = subparsers.add_parser("build", help="build the inverted index")

    args = parser.parse_args()
    print(args.command)

    match args.command:
        case "search":
            # print the search query here
            search_results = keyword_search.search_movies(args.query)
            print(search_results)
        case 'build':
            print("building")
            build_command()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()