# !/usr/bin/env python
# -*- coding: utf-8 -*-
# vim:set et ts=4 sw=4:
#
# Copyright (C) 2013 Ozan Çağlayan
# GPL License

import os
import sys
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
        print(("Usage: %s <duration> [ch1,ch2,..,chN]" % sys.argv[0]))
        return 1

    channels = None
    try:
        channels = sys.argv[2].split(",")
    except:
        pass

    # setup headset
    headset = epoc.EPOC(enable_gyro=False)
    if channels:
        headset.set_channel_mask(channels)

    # acquire
    idx, data = headset.acquire_data_fast(duration)

    print(("Battery: %d %%" % headset.battery))
    print("Contact qualities")
    print((headset.quality))

    # record
    utils.save_as_csv(data, headset.channel_mask)

    try:
        headset.disconnect()
    except e:
        print(e)

if __name__ == "__main__":
    sys.exit(main())
