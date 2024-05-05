import streamlit as st
import tempfile
import os
from model_functions import diagnoser, medicine_presciber
from st_audiorec import st_audiorec
# Import warnings just in case
import warnings
warnings.filterwarnings('ignore')

st.title('Respiratory Disease Diagnosis and Management System')
st.caption("### Created by Jawad028")

st.markdown("""
    ### Disclaimer
    This application is intended for educational purposes only and should not be used as a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
""")
# Ask for the user's name for display purposes but don't store it in user_data
user_name = st.text_input("Enter the patient's name:")

user_data = {
    'Age': st.number_input('Enter the age of the patient:', min_value=0, max_value=120, step=1),
    'Gender': st.radio('Enter Gender of the patient:', options=['Male', 'Female']),
    'Smoking Status': st.radio('Enter Smoking Status of the patient:',
                                options=['Active-smoker', 'Non-smoker', 'Ex-smoker'])
}

# Instructions before input method selection
st.markdown("**Audio Recording Instructions:**")
st.markdown("- Aim for a recording between 10 and 30 seconds.")
st.markdown("- Begin with normal breaths.")
st.markdown("- Then, inhale deeply, hold, exhale slowly.Repeat 2-3 times.")

play_sample_button = st.button("Play Sample Audio", key='play_sample_button')
if play_sample_button:
    with open("demo.wav", "rb") as f:
        sample_audio_bytes = f.read()
    st.audio(sample_audio_bytes, format="audio/wav")
   

input_method = st.selectbox(
    "Select your preferred input method:",
    options=['Upload audio file','Record audio' ]
)

if input_method == 'Record audio':
    st.markdown("*Beta: Results may vary!*")
    file = st_audiorec()
elif input_method == 'Upload audio file':
    file = st.file_uploader("Upload the audio file here", type=['wav', 'mp3'])

# Add the submit button
submitted = st.button("Submit")


if submitted and file is not None:
    #st.audio(file, format='audio/wav', start_time=0)
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
        if isinstance(file, bytes):  # This condition checks if the file is already a bytes object
            tmp_file.write(file)
        else:
            tmp_file.write(file.getvalue())
        tmp_file_path = tmp_file.name

    try:
        disease = diagnoser(tmp_file_path)
        user_data['Disease'] = disease

        if disease != 'Healthy':
            medicine = medicine_presciber(user_data)
            st.success(f'{user_name}, the patient is diagnosed with {disease}.')

            # Create a visually appealing display for the prescription
            st.subheader(f'Prescription for {user_name}')
            for med_name, amount, frequency in medicine:
                st.markdown(f"**Medicine:** {med_name}")
                st.markdown(f"**Dosage:** {amount}")
                st.markdown(f"**Frequency:** {frequency}")
                
        else:
            st.success(f'{user_name} is Healthy.')

    except Exception as e:
        st.error(f"An error occurred while processing the audio file: {e}")

    finally:
        if os.path.isfile(tmp_file_path):
            os.unlink(tmp_file_path)
