#!/usr/bin/python3

# Props for this script go to Hans van Kranenburg, his script using btrfs is
# waaay shorter and more robust than mine which had been parsing output of a
# btrfs command line utility

import btrfs
import sys


def get_dev_extent(fs, devid, paddr, path):
    # we can't just simply search backwards... :|
    tree = btrfs.ctree.DEV_TREE_OBJECTID
    min_key = btrfs.ctree.Key(devid, btrfs.ctree.DEV_EXTENT_KEY, 0)
    max_key = btrfs.ctree.Key(devid, btrfs.ctree.DEV_EXTENT_KEY, paddr)
    for header, data in btrfs.ioctl.search_v2(fs.fd, tree, min_key, max_key):
        pass
    return btrfs.ctree.DevExtent(header, data)


def main():
    if len(sys.argv) != 4:
        print(f"""Usage:
        {sys.argv[0]} <btrfs_dev_id> <physical_address> <btrfs_mount_point>
        The devid can be gotten from `btrfs fi show` command""")
        exit(1)
    devid = int(sys.argv[1])
    paddr = int(sys.argv[2])
    path = sys.argv[3]

    with btrfs.FileSystem(path) as fs:
        dev_extent = get_dev_extent(fs, devid, paddr, path)

    print(f"INF: devid {devid} paddr {paddr} is part of {dev_extent}")
    print("NOTE: this won't work for RAID56!")
    way_into = paddr - dev_extent.paddr
    print(f"paddr is {way_into} bytes into that dev extent")
    print(f"logical/virtual address is {dev_extent.chunk_offset + way_into}")


if __name__ == '__main__':
    main()
