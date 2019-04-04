import os
import random
from six.moves import xrange
import argparse


def create_random_bootstrap_file(bootstrap_dir, file_name, bootstrap_size, seed):
    random.seed(seed)
    full_path = os.path.join(bootstrap_dir, file_name)
    with open(full_path, 'wb') as fp:
        fp.write(bytearray(random.getrandbits(8) for _ in xrange(bootstrap_size * 1024 * 1024)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate bootstrap file")
    parser.add_argument("--type", choices=['random', 'graph', 'trustchain'], default='random',
                        help="Create bootrstrap file with data of one of the types")
    parser.add_argument("--size_mb", type=int, default=25, help="Size of the bootstrap file")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random file")
    parser.add_argument("--file_name", default="bootstrap.block", help="Name of the bootstrap file")
    def_dir = os.path.join(os.path.expanduser(u"~"), u".Tribler")
    parser.add_argument("--dir", default=def_dir)

    args = parser.parse_args()

    if args.type == 'random':
        print("Generating file "+args.dir+"/"+args.file_name)
        if not os.path.exists(args.dir):
            os.mkdir(args.dir)
        create_random_bootstrap_file(args.dir, args.file_name, args.size_mb, args.seed)
    else:
        print("Unimplemented")

