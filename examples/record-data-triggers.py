import os
import sys
import time
import random
import csv
import threading
import pygame

try:
    from emotiv import epoc, utils
except ImportError:
    sys.path.insert(0, "..")
    from emotiv import epoc, utils

duration = 10 # duration in seconds for trigger thread 
sampling_rate = 128
stop_flag = False
data_eeg = []
lock = threading.Lock() 

def record_eeg(headset, eeg_file_path):
    global stop_flag, data_eeg
    print("[EEG] Starting EEG recording...")
    start_time_eeg = time.time() 

    while not stop_flag:
        sample = headset.get_sample()
        if sample:
            timestamp = time.time() - start_time_eeg
            row = [timestamp] + list(sample)
            with lock:
                data_eeg.append(row)
        time.sleep(1 / sampling_rate) # ensure constant sampling rate

    print("[EEG] EEG recording stopped.")
    with open(eeg_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Timestamp'] + headset.channel_mask)
        with lock: 
            writer.writerows(data_eeg)

def record_triggers(trigger_file_path, stimuli_images):
    global stop_flag

    print("[TRIGGERS] Initializing Pygame...")
    pygame.init()
    
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Stimuli Display")

    loaded_stimuli = {}
    for stimulus_name, img_path in stimuli_images.items():
        try:
            image = pygame.image.load(img_path).convert()
            image = pygame.transform.scale(image, (screen_width // 2, screen_height // 2)) 
            loaded_stimuli[stimulus_name] = image
        except pygame.error as e:
            print(f"Error loading image {img_path}: {e}")
            return 

    print("[TRIGGERS] Starting stimuli display...")
    with open(trigger_file_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Stimulus', 'Trigger Type', 'Timestamp'])

        start_time_triggers = time.time()

        for i in range(duration): 
            if stop_flag: # allow early exit if EEG thread finishes first
                break

            stimulus = random.choice(list(loaded_stimuli.keys()))
            image_to_display = loaded_stimuli[stimulus]

            # clear screen
            screen.fill((0, 0, 0)) 

            # center the image
            image_rect = image_to_display.get_rect(center=(screen_width // 2, screen_height // 2))
            screen.blit(image_to_display, image_rect)

            pygame.display.flip()

            trigger_type = 1 if stimulus == "happy" else -1
            timestamp = time.time() - start_time_triggers

            writer.writerow([stimulus, trigger_type, timestamp])
            print(f"[TRIGGER] {stimulus} @ {timestamp:.4f}")

            # keep the stimulus on screen for a specific duration 
            time.sleep(0.5)

            screen.fill((0, 0, 0)) # clear for next stimulus or blank period
            pygame.display.flip()
            time.sleep(0.5) # blank screen for 0.5 seconds, totaling 1 second per trial

    print("[TRIGGERS] Stimuli display stopped.")
    pygame.quit() 

def main():
    global stop_flag

    headset = epoc.EPOC(enable_gyro=False)
    timestamp_run = time.strftime("%d-%m-%Y_%H-%M-%S")

    if not os.path.exists('results'):
        os.makedirs('results')

    eeg_file_path = f'results/emotiv-{timestamp_run}_eeg_data.csv'
    trigger_file_path = f'results/emotiv-{timestamp_run}_triggers.csv'
    stimuli_images = {
        "happy": "stimuli/happy1.jpg", 
        "sad": "stimuli/sad1.jpg"
    }

    # start threads
    eeg_thread = threading.Thread(target=record_eeg, args=(headset, eeg_file_path))
    trigger_thread = threading.Thread(target=record_triggers, args=(trigger_file_path, stimuli_images))

    eeg_thread.start()
    trigger_thread.start()

    # wait for the trigger thread to finish 
    trigger_thread.join()
    stop_flag = True # signal EEG thread to stop
    eeg_thread.join() # wait for EEG thread to finish writing data

    headset.disconnect()
    print("=== Recording complete ===")

if __name__ == "__main__":
    main()
