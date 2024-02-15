import numpy as np
import librosa #for audio processing
import pandas as pd
import pickle



def feature_extraction(file,max_pad_len=926,n_features=52):
    
    audio, sample_rate = librosa.load(file)
    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate,n_mfcc=n_features)
    
    if (mfccs.shape[1] < max_pad_len):
        pad_width = max_pad_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        
    elif (mfccs.shape[1] > max_pad_len):
        mfccs = mfccs[:, :max_pad_len]
      
    #adding one more dimension(1,52,926) to the mfccs needed for the model when working with single file
    mfccs=np.expand_dims(mfccs,axis=0)
      
    return mfccs



def prep():
    print("Preprocessing the data")