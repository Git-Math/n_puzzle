import sys

def error(*args):
    print('error: %s' % args, file=sys.stderr)
    sys.exit(1)
