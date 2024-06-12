
from argparse import ArgumentParser
from xnb import XNBReader

def parse_args():
    parser = ArgumentParser('xnb', description='Convert XNB files to a usable format')
    parser.add_argument('input', help='Input file')
    parser.add_argument('output', help='Output file')
    return parser.parse_args()

def main():
    args = parse_args()
    reader = XNBReader.from_file(args.input)
    reader.save(args.output)

if __name__ == '__main__':
    main()
