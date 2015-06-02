import argparse
from report import report


if __name__ == "__main__":

    # parsing command line
    parser = argparse.ArgumentParser(description='Ocean modelling program')
    parser.add_argument('path', type=str,
                        help='path to configuration file')
    parser.add_argument('iters', type=int,
                        help='number of iterations')
    parser.add_argument('mode', type=str,
                        help='"display" or "statistics" mode')
    args = parser.parse_args()
    config_file = args.path

    if args.mode == 'statistics':
        report(config_file, args.iters)
    elif args.mode == 'display':
        report(config_file, args.iters, statistics_mode=False, display_mode=True)
