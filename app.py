from __future__ import unicode_literals
from cgitb import text
from yt_dlp import YoutubeDL
import yt_dlp
import whisper
import pandas as pd
from moviepy.editor import VideoFileClip
import moviepy.editor as mp
from moviepy.editor import *
from moviepy.video.tools.subtitles import SubtitlesClip
import os

import cv2
from os import listdir
from os.path import isfile, join
from werkzeug.utils import secure_filename
import shutil
import argparse
import torch
import torchvision.transforms as transforms
from PIL import Image
from flask import Flask, jsonify, request, render_template, redirect, url_for

import sys


UPLOAD_FOLDER = 'inputs/vids'
ALLOWED_EXTENSIONS = {'mp4', 'mov', 'webm', 'ts', 'avi', 'y4m', 'mkv'}

app = Flask(__name__,static_folder='results')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/", methods = ['GET', 'POST'])
def index():
    return redirect(url_for('upload_file'))

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/upload", methods = ['GET', 'POST'])
def upload_file():

    # print(request.args.get('key', ''))
    source = 'inputs/vids'
    # destination = 
    out = 'results/subbed_vids/'
    opts_aud = {'format': 'mp3/bestaudio/best','keep-video':True, 'outtmpl': f'inputs/audio/audio.mp3', 'postprocessors': [{'key': 'FFmpegExtractAudio','preferredcodec': 'mp3'}]}
    vid_opts = {'format': 'mp4/bestvideo/best','outtmpl': f'{source}/video.mp4'}
    for f in os.listdir(source):
        os.remove(os.path.join(source, f))
    # for f in os.listdir(destination):
    #     os.remove(os.path.join(destination, f))
    # for f in os.listdir(out):
        # os.remove(os.path.join(out, f))
    try:
        text1 = request.form.values()
        text1 = list(text1)
        with YoutubeDL(vid_opts) as ydl:
            ydl.download(text1)
        with YoutubeDL(opts_aud) as ydl:
            ydl.download(text1)
    except:
        None
    
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            if 'video.mp4' in os.listdir('inputs/vids/'):
                return redirect(url_for('main', name='inputs/vids/video.mp4'))
            print('No file part')
            return redirect(request.url)
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            print('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], 'video.mp4'))
            return redirect(url_for('main', name='video.mp4'))
    return '''
   <!doctype html>
    <html>
    <style>
        #Geek_p {
            font-size: 30px;
            color: green;
        }
    </style>

    <body style="text-align:center;">

        <h1 style="color:blue;">
            Whisper AutoCaption
        </h1>

        <body>
            <div>
                Use Whisper AutoCaption to automatically subtitle your videos in a variety of languages
            </div>
            <div>
                After you select the video, click submit to run the model and add subtitles. 
            </div>
            <br>
            <div>
                <form method=post enctype=multipart/form-data>
                    <input type=file name=file>
                    <input type=submit value=Upload>
                </form>
            </div>
            <div>
            <form method="POST">
                Alternatively, you can also submit any Youtube video using the URL submission box below.
                <input name="text">
                <br>
                <br>
                <input type="submit">
            </form>
            </div>
        </body>
    </html>
    '''

@app.route("/play")
def playvideourl(filename): 
    return render_template('index.html', 
        movie_name='inputs/video/video.mp4',
        movie_ext='mp4')

@app.route('/main', methods=['POST','GET'])
def main():    
    # parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    # parser.add_argument("--audio_file", nargs="+", type=str, help="audio file(s) to transcribe")
    # parser.add_argument("--model_type", default="small", choices=['tiny', 'small', 'base', 'medium','large','tiny.en', 'small.en', 'base.en', 'medium.en'], help="name of the Whisper model to use")
    # parser.add_argument("--device", default="cuda" if torch.cuda.is_available() else "cpu", help="device to use for PyTorch inference")
    # parser.add_argument("--output", "-o", type=str, default=".", help="directory to save the outputs")
    # parser.add_argument("--download", default = True, help="bool, get files")
    # parser.add_argument("--url", default = None, help="youtube file")
    # parser.add_argument("--input_file", default = 'video.mp4', help="bool, get files")

    # parser.add_argument("--task", type=str, default="transcribe", choices=["transcribe", "translate"], help="whether to perform X->X speech recognition ('transcribe') or X->English translation ('translate')")


    # my_clip = mp.VideoFileClip('inputs/vids/video.mp4')
    # if len(os.listdir('inputs/audio')) == 0:
    #     my_clip.audio.write_audiofile('inputs/audio/audio.mp3', codec="libmp3lame")
    

    # # Instantiate whisper model using model_type variable
    # model = whisper.load_model('base')
    
    # # Get text from speech for subtitles from audio file
    # result = model.transcribe(f'inputs/audio/audio.mp3', task = 'translate')
    
    # # create Subtitle dataframe, and save it
    # dict1 = {'start':[], 'end':[], 'text':[]}
    # for i in result['segments']:
    #     dict1['start'].append(int(i['start']))
    #     dict1['end'].append(int(i['end']))
    #     dict1['text'].append(i['text'])
    # df = pd.DataFrame.from_dict(dict1)
    # # df.to_csv(f'experiments/{name}/subs.csv')
    # vidcap = cv2.VideoCapture('inputs/vids/video.mp4')
    # success,image = vidcap.read()
    # height = image.shape[0]
    # width =image.shape[1]

    # # Instantiate MoviePy subtitle generator with TextClip, subtitles, and SubtitlesClip
    # generator = lambda txt: TextClip(txt, font='P052-Bold', fontsize=width/50, stroke_width=.7, color='white', stroke_color = 'black', size = (width, height*.25), method='caption')
    # # generator = lambda txt: TextClip(txt, color='white', fontsize=20, font='Georgia-Regular',stroke_width=3, method='caption', align='south', size=video.size)
    # subs = tuple(zip(tuple(zip(df['start'].values, df['end'].values)), df['text'].values))
    # subtitles = SubtitlesClip(subs, generator)
    
    # # Ff the file was on youtube, add the captions to the downloaded video
    
    # video = VideoFileClip('inputs/vids/video.mp4')
    # final = CompositeVideoClip([video, subtitles.set_pos(('center','bottom'))])
    # final.write_videofile(f'results/subbed_vids/video.mp4', fps=video.fps, remove_temp=True, codec="libx264", audio_codec="aac")

    onlyfiles = [f for f in listdir('results/subbed_vids') if isfile(join('results/subbed_vids', f))]
    try:
        # onlyfiles.remove('.DS_Store')
        return playvideourl('inputs/video/video.mp4')
        # return render_template("index.html", variable = onlyfiles[0])
    except:
        return playvideourl('inputs/video/video.mp4')
        # return render_template("index.html", variable = onlyfiles[0])




if __name__ == '__main__':
    app.debug = True
    app.run(host="0.0.0.0")
    main()
    