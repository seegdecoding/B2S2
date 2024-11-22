import glob
import numpy as np
from scipy.stats import pearsonr



gen_mel = ['Samples_Predict_Mel.npy']
gt_mel = ['Samples_GT_Mel.npy']


cor_list = []
for i in range(len(gen_mel)):
    gen = np.load(gen_mel[i])
    gt = np.load(gt_mel[i])
    gt = gt[:gen.shape[0], :]
    
    cor = pearsonr(gen.flatten(), gt.flatten())
    cor_list.append(cor[0])

print('Correlation of BrainTalker:', np.mean(cor_list))


new_cor_list = []
for i in range(len(gen_mel)):
    gen = np.load(gen_mel[i])
    gt = np.load(gt_mel[i])
    gt = gt[:gen.shape[0], :]
    bin_correlation = []
    for bin in range(gen.shape[1]):
        cor = pearsonr(gen[:, bin], gt[:, bin])
        bin_correlation.append(cor[0])
    new_cor_list.append(np.mean(bin_correlation))

print('Correlation of Our Method:', np.mean(new_cor_list))
