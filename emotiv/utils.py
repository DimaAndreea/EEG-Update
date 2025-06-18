# -*- coding: utf-8 -*-
# vim:set et ts=4 sw=4:
#
# Copyright (C) 2012 Ozan Çağlayan
# GPL License

from scipy.io import savemat 
import numpy as np
import os
import time
import pandas as pd
from datetime import datetime

def check_packet_drops(seq_numbers):
    lost = []
    for seq in range(len(seq_numbers) - 1):
        cur = int(seq_numbers[seq])
        _next = int(seq_numbers[seq + 1])
        if ((cur + 1) % 128) != _next:
            lost.append((cur + 1) % 128)
    return lost

def get_level(raw_data, bits):
    """Returns signal level from raw_data frame."""
    level = 0
    for i in range(13, -1, -1):
        level <<= 1
        b, o = (bits[i] // 8) + 1, bits[i] % 8
        level |= (raw_data[int(b)] >> o) & 1

    return 0.51 * level

def save_as_csv(_buffer, channel_mask, metadata=None, filename=None):
    """
    Save EEG data to a CSV file, with optional metadata.
    """
    data = _buffer # shape (samples, channels)
    df = pd.DataFrame(data, columns=channel_mask)

    if metadata and "Initials" in metadata:
        date_info = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"emotiv-{metadata['Initials']}-{date_info}.csv"
    else:
        date_info = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        filename = f"emotiv-{date_info}.csv"

    df.to_csv(filename, index=False)

