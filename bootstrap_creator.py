import argparse
import pathlib
import os
import random


def create_random_bootstrap_file(bootstrap_dir, file_name, bootstrap_size, seed):
    random.seed(seed)
    full_path = pathlib.Path(bootstrap_dir, file_name)
    with open(full_path, 'wb') as fp:
        fp.write(bytearray(random.getrandbits(8) for _ in range(bootstrap_size * 1024 * 1024)))


if __name__ == '__main__':

    parser = argparse.ArgumentParser(description="Generate bootstrap file")
    parser.add_argument("--type", choices=['random', 'graph', 'trustchain'], default='random',
                        help="Create bootrstrap file with data of one of the types")
    parser.add_argument("--size_mb", type=int, default=25, help="Size of the bootstrap file")
    parser.add_argument("--seed", type=int, default=42, help="Seed for random file")
    parser.add_argument("--file_name", default="bootstrap.block", help="Name of the bootstrap file")
    def_dir = pathlib.Path(pathlib.Path.home(), ".Tribler")
    parser.add_argument("--dir", default=def_dir)

    args = parser.parse_args()

    if args.type == 'random':
        print(f"Generating file {args.dir}/{args.file_name}")
        path = pathlib.Path(args.dir)
        try:
            path.mkdir()
        except FileExistsError:
            # If the directory already exists then nothing needs to be done
            pass
        create_random_bootstrap_file(args.dir, args.file_name, args.size_mb, args.seed)
    else:
        print("Unimplemented")

