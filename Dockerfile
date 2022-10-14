FROM python:3.8-slim-buster

RUN apt-get update \
  && apt-get install -y wget \
  && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y git
RUN pip install flask
RUN pip install Werkzeug
RUN pip install numpy
RUN pip install torch==1.11.0+cu113 torchvision==0.12.0+cu113 -f https://download.pytorch.org/whl/torch_stable.html
RUN pip install tqdm 
RUN pip install more-itertools
RUN pip install transformers>=4.19.0
RUN pip install opencv-python-headless
RUN pip install ffmpeg-python
RUN apt install ffmpeg -y
RUN pip install git+https://github.com/openai/whisper.git 
RUN pip install yt-dlp pandas
RUN pip install moviepy --upgrade 
RUN apt install imagemagick -y 
RUN sed -i '88d' ~/../etc/ImageMagick-6/policy.xml 
WORKDIR Whisper-AutoCaption/
RUN git clone https://github.com/gradient-ai/Whisper-AutoCaption
RUN pip install -r Whisper-Autocaption/requirements.txt



EXPOSE 5000
CMD python app.py