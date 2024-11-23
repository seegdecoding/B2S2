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


For the newly added participant data, please visit: **https://zenodo.org/records/14179222**
For the sEEG data encompassing all participants, please visit: **https://zenodo.org/records/13332808**

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
The [checkpoint](https://drive.google.com/file/d/1qKT6dofCuIqPtRI43FAPcbS12mj9IrfP/view?usp=sharing) file should be placed in the mel2wav/checkpoints/ directory

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

## others
We would like to clarify a key difference in the computation of the Pearson correlation coefficient between our evaluation method and that used in Brain Talker. In Brain Talker, the Pearson correlation is calculated by first flattening both the predicted and ground truth Mel spectrograms, which have dimensions T×F, into one-dimensional arrays of size 1×(T×F). The correlation is then calculated between these flattened arrays, and the resulting coefficients are averaged across all samples.
In contrast, our evaluation method calculates the Pearson correlation by comparing the predicted and true frequencies at each corresponding time point. For each sample, we compute the Pearson correlation coefficients across the frequency dimension (1×F) for each time step, performing this comparison T times. These coefficients are averaged over the T time steps, and then averaged again across all samples to derive the overall Pearson correlation.
We believe that for Mel spectrograms, which inherently possess a structured frequency component, computing the Pearson correlation column-wise is more appropriate. This approach evaluates the alignment of the predicted and ground truth spectrograms at the frequency channel level, providing a more rigorous assessment of the model's performance. While adopting the calculation method from [BrainTalker](https://github.com/braintalker/braintalker_pytorch) would also yield high Pearson correlation coefficients for our results, it is less indicative of the fidelity of Mel spectrograms in capturing detailed frequency alignments.
To illustrate, we have provided scripts for both testing methods on our [GitHub](https://github.com/seegdecoding/B2S2) repository under Calculate_Mel.py. When applied to Samples_GT_Mel.npy and Samples_Predict_Mel.npy, the Pearson correlation calculated using the BrainTalker method resulted in a coefficient of 0.848, whereas our method yielded a coefficient of 0.644.
