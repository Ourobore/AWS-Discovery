import sys

import dotenv

from domain.create_database_item import create_database_item
from domain.generate_json_file import generate_json_file
from domain.generate_laptop import generate_laptop
from domain.push_upload_message_on_queue import push_upload_message_on_queue
from domain.upload_file_to_storage import upload_file_to_storage

dotenv.load_dotenv()


def main(filename: str, payload: dict):
    try:
        generate_json_file(filename, payload)
    except OSError as e:
        print(f"Can't generate file {filename}: {e}", file=sys.stderr)
        exit(1)

    print(payload)

    create_database_item(payload)
    upload_file_to_storage(filename)
    push_upload_message_on_queue(payload["uuid"], filename)


if __name__ == "__main__":
    args = sys.argv[1:]
    match len(args):
        case 1:
            filename = args[0]
        case 0:
            print("A name for the generated JSON file must be specified", file=sys.stderr)
            exit(1)
        case _:
            print("Too many arguments were specified: only a filename is required", file=sys.stderr)
            exit(1)

    main(filename=filename, payload=generate_laptop())
