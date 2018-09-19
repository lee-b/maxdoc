import argparse


def get_config(argv):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--output-format')

    args = argparser.parse_args(argv[1:])

    return args
