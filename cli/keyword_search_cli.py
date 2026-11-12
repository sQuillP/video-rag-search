import argparse
from lib import keyword_search


# https://www.boot.dev/lessons/b05a1f24-785d-474f-b935-a5fea8b564d3

def build_command():
    indices = keyword_search.InvertedIndex()
    loaded = indices.load()
    if loaded == False:
        print('Unable to load indices... check the logs. Shutting down program...')
        exit(1)
    return indices

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

    indices = build_command()

    match args.command:
        case "search":
            # print the search query here
            search_results = keyword_search.search_movies(args.query, indices, 5)
            for entry in search_results:
                print(entry['id'], '->', entry['content'][:20])
        case 'build':
            print("building")
            build_command()
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()