# Emotiv EPOC Python Interface (Modified)

**Original Author:** Ozan Çağlayan, Galatasaray University, Computer Engineering Dept.
*This project is a modified version of the original 'python-emotiv' library by Ozan Çağlayan.*

---

## Original Project Overview

`python-emotiv` is an open-source library initially developed to acquire data from Emotiv EPOC headset. It uses a reverse-engineered protocol (not the official Emotiv SDK) and `libusb` for dongle access, making it suitable for deployment on ARM boxes like Raspberry Pi.

Parts of the project are inspired by [mushu](https://github.com/venthur/mushu) and [emokit](https://github.com/openyou/emokit).

## Key Dependencies (Original)

* [pyusb](http://sourceforge.net/projects/pyusb) (Version >= 1.0)
* [pycrypto](https://www.dlitz.net/software/pycrypto)
* numpy
* scipy
* matplotlib (For data analysis scripts under utils/)
* BeagleBone Black GPIO (For SSVEP BCI in examples/)

---

## My Project's Dependencies

* [pyusb](https://pypi.org/project/pyusb/) 
* [pycrypto](https://pypi.org/project/pycryptodome/) 
* [numpy](https://numpy.org/) 
* [pandas](https://pandas.pydata.org/) 
* [pygame](https://www.pygame.org/news) 
* [mne](https://mne.tools/stable/index.html) 
* [matplotlib](https://matplotlib.org/)

---

## My Contributions and Modifications (Andreea Dima)

This repository extends the original `python-emotiv` project to enable real-time EEG data acquisition and Event-Related Potential (ERP) analysis for psychological experiments.

Key modifications and additions include:

1.  **Python 2 to Python 3 Migration:**
    * The original codebase was updated from Python 2 to Python 3 using the `2to3` tool, ensuring compatibility with modern environments.
  
2.  **CSV Data Export:**
    * Changed the data export format from `.mat` (MATLAB) to `.csv` files for both EEG signals and triggers. This facilitates easier integration with standard Python analytical        tools like Pandas and MNE-Python.
  
      
3.  **Synchronized Stimulus Presentation and Trigger Recording:**
    * Implemented visual stimulus presentation using `pygame` (e.g., happy/sad images).
    * Developed a triggering system that records stimulus type (e.g., `+1` for happy, `-1` for sad) and precise timestamps alongside EEG data.
    * Utilized Python `threading` to enable simultaneous recording of EEG and stimulus presentation.


---
### Recording Data

To record EEG data synchronized with stimulus presentation:

1.  **Prepare Stimuli:** Ensure your stimulus images (e.g., `happy1.jpg`, `sad1.jpg`) are placed in a folder named `stimuli/` in the root directory of the project.
2.  **Run the Acquisition Script:** Open terminal, navigate into the `examples/` directory, and execute the recording script.

    **Important Note on Permissions:**
    Due to low-level USB access requirements for the Emotiv headset on Linux, the acquisition script often requires elevated privileges. Therefore, it typically needs to be run using `sudo`.
    

4.  **Output Files:** After the recording duration ends, two `.csv` files will be saved in the `results/` directory.

