# CerebroVoice: A Stereotactic EEG Dataset and Benchmark for Bilingual Brain-to-Speech Synthesis and Activity Detection
**CerebroVoice** is the first publicly available stereotactic EEG (sEEG) dataset designed for bilingual brain-to-speech synthesis and voice activity detection (VAD). The dataset includes neural recordings collected while two bilingual participants (Mandarin and English speakers) read aloud Chinese Mandarin words, English words, and Chinese Mandarin digits. This dataset enables research into brain-to-speech synthesis, bilingual speech decoding, and voice activity detection from sEEG signals.
This repository provides the dataset, benchmarks, and code for running experiments on bilingual brain-to-speech synthesis using the **Mixture of Bilingual Synergy Experts (MoBSE)** framework, as well as for voice activity detection (VAD) using standard EEG models.

---
## **Environment Setup**

To run the experiments and use the dataset, follow these steps to set up the environment.

### **1. Clone the Repository**
Clone this repository to your local machine:
```bash
git clone https://github.com/seegdecoding/B2S2.git
cd B2S2
```

### Install Dependencies
Make sure you have Python 3.7+ installed. It’s recommended to use a virtual environment.
```bash
pip install -r requirements.txt
```
## **Dataset**

The **CerebroVoice** dataset is available for download. The dataset includes sEEG recordings and their corresponding audio samples for two subjects (Mandarin and English). Each recording contains speech data across various tasks (Mandarin words, English words, and Chinese Mandarin digits).

You can download the dataset from the following links:
- [Dataset Link](https://zenodo.org/records/13332808)
- [GitHub Dataset](https://github.com/Brain2Speech2/B2S2)

### EEG Preprocessing

**Preprocess and Save Features**:
To preprocess the EEG data and save the relevant features, you can execute the following Python script:
```python
python preprocess_eeg.py
```
Moreover, you have the flexibility to modify the code within this script in order to choose different features, such as BBS, HGA, and LFS.

### Mel2wav

**Reconstruct Audio from Synthesis Mel-spectrograms**:
If you want to reconstruct audio from the synthesized mel-spectrograms, you can use the following Python script:
```python
python mel2wav.py
```
It should be noted that you need to download the checkpoint of our pretrained model from the link provided below: 
The checkpoint file should be placed in the mel2wav/checkpoints/ directory

### **Dataset Structure**
The dataset is organized as follows:
```bash
CerebroVoice/
    ├── Subject1/
    │   ├── BBS/
    │   ├── HGA/
    │   ├── LFS/
    │   ├── MEL/
    │   └── SEEG/
    ├── Subject2/
    │   ├── BBS/
    │   ├── HGA/
    │   ├── LFS/
    │   ├── MEL/
    │   └── SEEG/
    └── README.md
```
- **MEL**: Mel-spectrograms of the audio.
- **SEEG**: Preprocessed sEEG signals.
- **BBS/HGA/LFS**: Different frequency bands used for the synthesis (Broadband, High Gamma Activity, Low-Frequency Signals).


## **Metrics**

### **Pearson Correlation Coefficient**:

In our evaluation method, the **Pearson correlation coefficient** is calculated on a frame-by-frame basis for each Mel spectrogram. Specifically, for each predicted and ground truth Mel spectrogram, we compute the Pearson correlation coefficient for each frame (T×F), and then average the correlation coefficients across all frames. 
This method preserves the temporal structure of the Mel spectrograms and avoids the loss of information that can occur when flattening the spectrograms. This frame-by-frame correlation provides a more detailed and accurate evaluation of the predicted spectrograms in the context of brain-to-speech synthesis.

