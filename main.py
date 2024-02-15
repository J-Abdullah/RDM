import warnings
warnings.filterwarnings('ignore')
from model_functions import *
from input_functions import *

print('Welcome to the Respiratory Disease Diagnosis and Prescription System')

print('Please enter the following details of the patient:')

user_data={}
user_data['Age']=input('Enter the age of the patient: ')
user_data['Gender']=input('Enter Gender of the patient: ')
user_data['Smoking Status']=input('Enter Smoking Status of the patient: ')


user_input=input('I you want to recored the patient\'s audio, press 1.\nIf you want to upload the audio file, press 2')

if user_input=='1':
    file=record_audio()
else:
    file=select_file()

#file=r'E:\Lea!n\RDM\Respiratory_Sound_Database\audio_and_txt_files\107_2b4_Al_mc_AKGC417L.wav'
#file=select_file()
disease=diagnoser(file)

user_data['Disease']= disease

if disease!='Healthy':
    medicine=medicine_presciber(user_data)
    print('The patient is diagnosed with',disease)
    print('The patient is prescribed with',medicine)
else:
    print('The patient is Healthy')