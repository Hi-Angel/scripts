#!/usr/bin/python3

### Compares two files that are outputs of `/proc/diskstats`, and prints the amount
### of bytes read/write that changed for devices between the two.

import sys

if len(sys.argv) != 3:
    print("Wrong number of arguments, expected 2, got ", len(sys.argv)-1)
    sys.exit(-1)

i_col_device_name     = 2
i_col_sectors_written = 9
i_col_time_writing_ms = 10
i_col_sectors_read    = 5
i_col_time_reading_ms = 6

class Stats:
    def __init__(self, line):
        cols = line.split()
        self.device_name     = cols[i_col_device_name]
        self.sectors_written = int(cols[i_col_sectors_written])
        self.time_writing_ms = int(cols[i_col_time_writing_ms])
        self.sectors_read    = int(cols[i_col_sectors_read])
        self.time_reading_ms = int(cols[i_col_time_reading_ms])


def create_stats(stats_file):
    with open(stats_file) as f:
        return [Stats(line) for line in f.readlines() if line.strip()]

dev_stats_older = create_stats(sys.argv[1])
dev_stats_newer = create_stats(sys.argv[2])
assert len(dev_stats_older) == len(dev_stats_newer),\
       'Don\'t know what to compare, the number of non-empty lines is different before- and after-'

def sectors_to_human_readable(n_sectors):
    KB = 1024
    MB = 1024**2
    GB = 1024**3
    n_bytes = n_sectors * 512
    return f"{n_bytes / GB: .3f} GB" if n_bytes > GB else\
           f"{n_bytes / MB: .3f} MB" if n_bytes > MB else\
           f"{n_bytes / KB: .3f} KB" if n_bytes > KB else\
           f"{n_bytes}"

def ms_to_sec(ms):
    return ms / 1000

for before,after in zip(dev_stats_older, dev_stats_newer):
    assert(before.device_name == after.device_name)
    print(f'''{before.device_name}:
              Written: {sectors_to_human_readable(after.sectors_written - before.sectors_written)}
              Time spent writing: {ms_to_sec(after.time_writing_ms - before.time_writing_ms)} sec
              Read: {sectors_to_human_readable(after.sectors_read - before.sectors_read)}
              Time spent reading: {ms_to_sec(after.time_reading_ms - before.time_reading_ms)} sec''')
