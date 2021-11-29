FROM python:3.8

WORKDIR /chopchop_li_2021

RUN pip install --upgrade pip \
 && pip install numpy tensorflow pandas==1.2.2 bio

# Add script
ADD . .
COPY dockers/Cas9Emulation.py .
ENV PYTHONPATH .

ENTRYPOINT ["python","./dockers/chopchop_li_2021/run_croton_prediction.py"]

