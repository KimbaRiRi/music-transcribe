import time
from pytube import YouTube
from streamlit_player import st_player

from DrumTranscriber import DrumTranscriber
from utils.config import SETTINGS

import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import matplotlib.pyplot as plt

import librosa
import librosa.display

# from midigen import create_midi

from midigen import create_drum_midi

# def get_title(input):
#     return YouTube(input).title


@st.experimental_memo
def get_predictions(input, start_from=0):
    yt = YouTube(input)

    video = yt.streams.filter(only_audio=True).first()

    out_file = video.download(output_path=".")

    base, ext = os.path.splitext(out_file)
    new_file = base + '.wav'
    os.rename(out_file, new_file)

    # samples, sr = librosa.load(
    #     new_file, sr=44100, duration=30, offset=start_from)
    samples, sr = librosa.load(
        new_file, sr=None, duration=60, offset=start_from)
    st.audio(samples, sample_rate=sr)

    os.remove(new_file)

    preds = transcriber.predict(samples, sr)

    return preds, samples, sr


@st.experimental_singleton
def initialise_transcriber():
    transcriber = DrumTranscriber()

    return transcriber


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')


# def export_midi(title, part):
#     return os.path.join("output", title + "-" + part + ".mid")

transcriber = initialise_transcriber()

st.title('Drum Transcriber Demo')

input = st.text_input('Input youtube link here',
                      value='https://www.youtube.com/watch?v=k6BVnvgoECY')
start_from = st.number_input(label='Start from (in seconds)', min_value=0)

if input:
    st_player(input)

preds = None

if input and start_from is not None:
    st.title('Predictions')
    preds, samples, sr = get_predictions(input, start_from)

    labelled_preds = [SETTINGS['LABELS_INDEX'][i] for i in
                      np.argmax(
                          preds[SETTINGS['LABELS_INDEX'].values()].to_numpy(), axis=1)
                      ]

    preds['prediction'] = labelled_preds
    preds['confidence'] = preds.apply(
        lambda x: f"{x[x['prediction']]*100:.1f}%", axis=1)
    preds['time'] = preds['time'].round(2)

    st.write(preds[['time', 'prediction', 'confidence']].T)

    fig, ax = plt.subplots(sharex=True, nrows=7, figsize=(20, 20))

    librosa.display.waveshow(
        samples, sr=sr, offset=start_from, ax=ax[0])

    ax[0].set_yticklabels([])
    ax[0].set_xlabel(None)

    # tempo = int(round(60000000 / librosa.beat.tempo(y=samples, sr=sr)[0]))
   


    for i in range(1, 7):
        label_name = SETTINGS['LABELS_INDEX'][i-1]

        hit_times = np.array(
            preds[preds['prediction'] == label_name]['time'].to_list())

        ax[i].vlines(hit_times+start_from, -1, 1)
        ax[i].set_ylabel(label_name, rotation=0, fontsize=20)
        ax[i].set_yticklabels([])

       

        if i == 6:
            ax[i].set_xlabel('time')
            ax[i].set_xlabel('time')

    st.pyplot(fig)

    st.download_button(
        "Press to Download",
        convert_df(preds),
        "predictions.csv",
        "text/csv",
        key='download-csv'
    )

    st.write(preds, use_container_width=True)

    # Example usage
    csv_file_path = 'csv/predictions-3d.csv'
    midi_file_path = 'midi/output.mid'

    create_drum_midi(csv_file_path, midi_file_path, bpm=108)


 # title = get_title(input)
     # filename = label_name + ".mid"
        # filepath = os.path.join(title, filename)
        # create_midi(hit_times, filepath, tempo)
