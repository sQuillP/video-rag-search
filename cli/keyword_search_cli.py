import argparse
from lib import keyword_search



def load_cached():
    indices = keyword_search.InvertedIndex()
    loaded = indices.load()
    if loaded == False:
        print('Unable to load indices... check the logs. Shutting down program...')
        exit(1)
    return indices


def build():
    indices = keyword_search.InvertedIndex()
    valid = indices.build()
    if valid:
        print('successfully built the indices')
    else:
        print('something went wrong building the indices')
    success = indices.save()
    if success:
        print('successfully saved the indices')
    else:
        print('unable to save the indices. Something went wrong...')


def tf(index:keyword_search.InvertedIndex, doc_id:int, term:str):
    token = index.tokenize_term(term)
    frequency = index.get_tf(doc_id, term)
    return frequency



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

    args = parser.parse_args()

    match args.command:
        case "search":
            indices = load_cached()
            # print the search query here
            search_results = keyword_search.search_movies(args.query, indices, 5)
            for entry in search_results:
                print(entry['id'], '->', entry['content'][:20])
        case 'build':
            print("building")
            build()
        case 'tf':
            indices = load_cached()
            result = tf(indices, args.doc_id, args.term)
            print(result)
        case _:
            parser.print_help()


if __name__ == "__main__":
    main()