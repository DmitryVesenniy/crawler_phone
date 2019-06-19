#!/usr/bin/python3

import os
import sys
import argparse
import concurrent.futures

from parser import worker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_urls(file_path):
    try:
        with open(file_path, 'r') as f:
            urls = f.read().split('\n')

    except Exception as err:
        print("Script Error: ", err)
        sys.exit(1)

    return urls


def main(file_path):
    urls = get_urls(file_path)
    result = set()

    if len(urls) == 0:
        print("Urls length = 0")
        sys.exit(0)

    print("Start parser ...")

    with concurrent.futures.ThreadPoolExecutor(50) as executor:
        exhaust = executor.map(worker, urls)

    for coll in exhaust:
        result.update(coll)

    print(result)

    print("... ThE EnD ...")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='--help')
    parser.add_argument('--path', type=str, required=True)
    args = parser.parse_args()

    main(args.path)
