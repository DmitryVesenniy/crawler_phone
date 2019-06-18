# -*- coding: utf-8 -*-
#!/usr/bin/python3

import os
import sys
import concurrent.futures

from parser import worker

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def get_urls():
    try:
        with open(os.path.join(BASE_DIR, "conf", "urls.txt"), 'r') as f:
            urls = f.read().split('\n')

    except Exception as err:
        print("Script Error: ", err)
        sys.exit(1)

    return urls


def main():
    urls = get_urls()

    if len(urls) == 0:
        print("Urls length = 0")
        sys.exit(0)

    print("Start parser ...")

    with concurrent.futures.ThreadPoolExecutor(50) as executor:
        executor.map(worker, urls)

    print("... ThE EnD ...")


if __name__ == "__main__":
    main()
