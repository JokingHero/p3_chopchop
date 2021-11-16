FROM python:3.8

WORKDIR /chopchop_li_2021

RUN pip install --upgrade pip \
 && pip install numpy tensorflow pandas==1.2.2

# Add script
ADD . .

ENTRYPOINT ["python", "./run_croton_prediction.py"]