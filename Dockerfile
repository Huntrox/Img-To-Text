FROM python:3.10-slim

ENV DEBIAN_FRONTEND=noninteractive


RUN apt-get update \
  && apt-get -y install tesseract-ocr

RUN apt update \
  && apt-get install ffmpeg libsm6 libxext6 -y
  
RUN pip3 install pytesseract
RUN pip3 install opencv-python
RUN pip3 install pillow

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]
CMD ["main.py","flask", "run", "--host", "0.0.0.0"]