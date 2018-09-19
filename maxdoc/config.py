import argparse


def get_config(argv):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output-format')
    argparser.add_argument('--renderer', default='html')
    argparser.add_argument('input_doc')

    args = argparser.parse_args(argv[1:])

    return args
