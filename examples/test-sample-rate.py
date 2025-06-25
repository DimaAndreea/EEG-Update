# !/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import time
import numpy as np

try:
    from emotiv import epoc, utils
except ImportError:
    sys.path.insert(0, "..")
    from emotiv import epoc, utils

def main():
    try:
        duration = int(sys.argv[1])
    except:
        print("Usage: %s <duration> [ch1,ch2,..,chN]" % sys.argv[0])
        return 1

    channels = None
    try:
        channels = sys.argv[2].split(",")
    except:
        pass

    headset = epoc.EPOC(enable_gyro=False)
    if channels:
        headset.set_channel_mask(channels)

    print("Starting sampling rate test...")

    count = 0
    start_time = time.time()
    all_data = []

    while time.time() - start_time < duration:
        sample = headset.get_sample()
        if sample is not None:
            all_data.append(sample)
            count += 1

    elapsed = time.time() - start_time
    print(f"Packets received in {elapsed:.2f} seconds: {count}")
    print(f"Estimated sampling rate: {count / elapsed:.2f} Hz")

    utils.save_as_csv(all_data, headset.channel_mask)

    try:
        headset.disconnect()
    except Exception as e:
        print(e)

if __name__ == "__main__":
    main()

