import argparse
import actions

parser = argparse.ArgumentParser(
    description="Improve the way you look at your picture collection with this simple CLI tool"
)

subparser = parser.add_subparsers()

generate = subparser.add_parser("generate", help="Generate the pictures")
generate.add_argument("dir", type=str, help="The directory where the tree of input picture starts")
generate.add_argument("save_dir", type=str, help="The directory where to save the output pictures")
generate.set_defaults(func=actions.process_dir)

copy = subparser.add_parser("copy", help="Copy the pictures to the output path without adding text")
copy.add_argument("dir", type=str, help="The directory where the tree of input picture starts")
copy.add_argument("save_dir", type=str, help="The directory where to save the output pictures")
copy.set_defaults(func=actions.copy)

args = parser.parse_args()

args.func(args) # Call the function requested by the user