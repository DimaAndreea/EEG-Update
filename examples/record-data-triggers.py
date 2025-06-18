import os
import sys
import time
import random
import csv
from PIL import Image

try:
    from emotiv import epoc, utils
except ImportError:
    sys.path.insert(0, "..")
    from emotiv import epoc, utils

def record_trigger(stimulus, trigger_type, timestamp, csv_writer):
    csv_writer.writerow([stimulus, trigger_type, timestamp])

def show_stimulus_and_trigger(stimulus, image_path, csv_writer):
    image = Image.open(image_path)
    image.show()

    trigger_type = 1 if stimulus == "happy" else -1
    timestamp = time.time()

    record_trigger(stimulus, trigger_type, timestamp, csv_writer)

    time.sleep(1)
    image.close()

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

    headset = epoc.EPOC(enable_gyro=False)
    if channels:
        headset.set_channel_mask(channels)

    timestamp = time.strftime("%d-%m-%Y_%H-%M-%S")
    if not os.path.exists('results'):
        os.makedirs('results')

    trigger_file_path = f'results/emotiv-{timestamp}_triggers.csv'
    eeg_file_path = f'results/emotiv-{timestamp}_eeg_data.csv'

    with open(trigger_file_path, 'w', newline='') as trigger_file:
        csv_writer = csv.writer(trigger_file)
        csv_writer.writerow(['Stimulus', 'Trigger Type', 'Timestamp'])

        stimuli = ["happy", "sad"]
        stimuli_images = {
            "happy": "stimuli/happy1.jpg",
            "sad": "stimuli/sad1.jpg"
        }

        for _ in range(duration):
            stimulus = random.choice(stimuli)
            show_stimulus_and_trigger(stimulus, stimuli_images[stimulus], csv_writer)

    idx, data = headset.acquire_data_fast(duration)

    sampling_rate = 128
    timestamps = [(i / sampling_rate) for i in range(len(data))]

    data_with_timestamps = []
    for i, row in enumerate(data):
        row_with_timestamp = [timestamps[i]] + list(row)
        data_with_timestamps.append(row_with_timestamp)

    with open(eeg_file_path, 'w', newline='') as eeg_file:
        eeg_writer = csv.writer(eeg_file)
        eeg_writer.writerow(['Timestamp'] + headset.channel_mask)
        eeg_writer.writerows(data_with_timestamps)

    try:
        headset.disconnect()
    except e:
        print(e)

if __name__ == "__main__":
    sys.exit(main())

