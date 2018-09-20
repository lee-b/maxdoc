import argparse
import logging


def get_config(argv):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output-format')
    argparser.add_argument('--renderer', default='html')
    argparser.add_argument('input_doc')
    argparser.add_argument('output_doc')

    args = argparser.parse_args(argv[1:])

    args.in_fp = open(args.input_doc)
    args.out_fp = open(args.output_doc, 'w')

    return args
