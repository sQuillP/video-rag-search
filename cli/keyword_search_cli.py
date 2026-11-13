import argparse
import math
from lib import keyword_search, commands





def main() -> None:
    parser = argparse.ArgumentParser(description="Keyword Search CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")
    
    # 1. Define search subparser
    search_parser = subparsers.add_parser("search", help="Search movies using keywords")
    search_parser.add_argument("query", type=str, help="Search query")

    # 2. Define build subparser with its own variable name
    build_parser = subparsers.add_parser("build", help="build the inverted index")

    tf_parser = subparsers.add_parser('tf', help='get the token frequency')
    tf_parser.add_argument('doc_id', type=int, help='Document id')
    tf_parser.add_argument('term', type=str, help='team to get the count for')

    idf_parser = subparsers.add_parser('idf', help='use the idf command')
    idf_parser.add_argument('term', type=str, help='term for idf')

    tfidf_parser = subparsers.add_parser('tfidf', help='Calculate the tfidf score')
    tfidf_parser.add_argument('doc_id', type=int, help='document id for tfidf to find')
    tfidf_parser.add_argument('term', type=str, help='tfidf term')
    args = parser.parse_args()

    match args.command:
        case "search":
            # print the search query here
            search_results = keyword_search.search_movies(args.query,commands.index, 5)
            for entry in search_results:
                print(entry['id'], '->', entry['content'][:20])
        case 'build':
            print("building")
            commands.build()
        case 'tf':
            result = commands.tf(args.doc_id, args.term)
            print(result)
        case 'idf':
            term = args.term
            result = commands.idf(term)
            print(f"Inverse document frequency of '{args.term}': {result:.2f}")
        case 'tfidf':
            tfidf_score = commands.tfidf(args.doc_id, args.term)
            print(f"TF-IDF score of '{args.term}' in document '{args.doc_id}': {tfidf_score:.2f}")
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()