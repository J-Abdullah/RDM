import numpy as np
import librosa #for audio processing
import pandas as pd
import pickle
from tensorflow.keras.models import load_model
from keras_self_attention import SeqSelfAttention
from sklearn.preprocessing import LabelEncoder
from tensorflow.keras.layers import LSTM, Dense, Dropout, Conv1D, MaxPooling1D, Input, BatchNormalization


#loading models and encoders
label_encoder=pickle.load(open(r'Serialized_objects\disease_encoder.pkl','rb'))

d_model=load_model(r'Serialized_objects\RDM_Diagnose.h5',custom_objects={'SeqSelfAttention': SeqSelfAttention})

user_encoder=pickle.load(open(r'Serialized_objects\user_data_encoder.pkl','rb'))

prescription_model=pickle.load(open(r'Serialized_objects\medication_prescription.pkl','rb'))


def feature_extraction(file_or_audio,max_pad_len=926,n_features=52):
    
    if isinstance(file_or_audio,str):
        audio, sample_rate = librosa.load(file_or_audio)
    elif isinstance(file_or_audio,tuple):
        audio,sample_rate=file_or_audio
    else:
        raise ValueError("Invalid input. Expected a file path or a tuple of (audio, sample_rate).")


    mfccs = librosa.feature.mfcc(y=audio, sr=sample_rate,n_mfcc=n_features)
    
    if (mfccs.shape[1] < max_pad_len):
        pad_width = max_pad_len - mfccs.shape[1]
        mfccs = np.pad(mfccs, pad_width=((0, 0), (0, pad_width)), mode='constant')
        
    elif (mfccs.shape[1] > max_pad_len):
        mfccs = mfccs[:, :max_pad_len]
      
    #adding one more dimension(1,52,926) to the mfccs needed for the model when working with single file
    mfccs=np.expand_dims(mfccs,axis=0)
      
    return mfccs

def diagnoser(file_or_audio):
    mfcc=feature_extraction(file_or_audio)
    disease=d_model(mfcc)
    disease=label_encoder.inverse_transform(np.argmax(disease,axis=1))[0]
    return disease



def medicine_presciber(user_data):
    #convert the user data to a dataframe
    user_df=pd.DataFrame([user_data])

    #encode the user data
    categorical_data=user_df[['Gender','Smoking Status','Disease']]
    numeric_data=user_df[['Age']]

    categorical_data=user_encoder.transform(categorical_data).toarray()
    features = np.hstack([numeric_data, categorical_data])
    
    medicine=prescription_model.predict(features)
    return medicine