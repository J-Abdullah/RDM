import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import sounddevice as sd
import numpy as np
import noisereduce as nr

def select_file():
    root=tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename()

def record_audio(duration=20, fs=22050):
    print('Recording...')
    audio = sd.rec(int(duration * fs), samplerate=fs, channels=1)
    sd.wait()
    print('Recording stopped')
    audio = np.squeeze(audio)
    
    # Reduce noise
    #audio = nr.reduce_noise(audio,fs)
    
    return audio, fs



def get_gender(user_data):
    def selected(event):
        user_data['Gender']=combo.get()
        root.quit()
    
    root=tk.Tk()
    root.title('Gender Selection')
    
    combo=ttk.Combobox(root,values=['Male','Female'])
    combo.current(0)
    combo.bind('<<ComboboxSelected>>',selected)
    combo.pack()
    
    root.mainloop()
    
def get_smoking_status(user_data):
    def selected(event):
        user_data['Smoking Status']=combo.get()
        root.quit()
    
    root=tk.Tk()
    root.title('Smoking Status')
    
    combo=ttk.Combobox(root,values=['Non-smoker','Active-smoker','Ex-smoker'])
    combo.current(0)
    combo.bind('<<ComboboxSelected>>',selected)
    combo.pack()
    
    root.mainloop()