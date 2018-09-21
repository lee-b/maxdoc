import argparse
import logging


class Config:
    def __init__(self, args):
        for k, v in args.__dict__.items():
            setattr(self, k, v)

        self.heading_level = 1

    def increment_heading_level(self):
        self.heading_level += 1
        return ''

    def decrement_heading_level(self):
        self.heading_level -= 1
        return ''


def get_config(argv):
    argparser = argparse.ArgumentParser()
    argparser.add_argument('--renderer', default='html')
    argparser.add_argument('--dump-transformed-ast', default=False, action="store_true")
    argparser.add_argument('input_doc')
    argparser.add_argument('output_doc')

    args = argparser.parse_args(argv[1:])

    args.in_fp = open(args.input_doc)
    args.out_fp = open(args.output_doc, 'w')

    return Config(args)
