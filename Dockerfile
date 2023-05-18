FROM python:3.11-slim-buster

RUN apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y git
RUN pip install flask
RUN pip install Werkzeug
RUN pip install numpy
RUN pip install torch==1.10.0 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install tqdm 
RUN pip install more-itertools
RUN pip install transformers>=4.19.0
RUN pip install opencv-python-headless
RUN pip install ffmpeg-python
RUN apt install ffmpeg -y
RUN pip install git+https://github.com/openai/whisper.git 
RUN pip install pandas
RUN pip install moviepy --upgrade 
RUN apt install imagemagick -y 
RUN sed -i '88d' ~/../etc/ImageMagick-6/policy.xml 
RUN git clone https://github.com/gradient-ai/Whisper-AutoCaption
WORKDIR Whisper-AutoCaption/
RUN pip install -r requirements.txt
RUN pip install -U yt-dlp
RUN find .paperspace/ -type f > listOfFiles.list

EXPOSE 5000
