FROM python:3.6

COPY . ./app

RUN apt update && apt install -y cmake && \
    cd ./app/dockers/chopchop_allen_2018/indel_analysis/indelmap &&  \
    cmake . -DINDELMAP_OUTPUT_DIR=/usr/local/bin && \
    make && make install

RUN pip install --upgrade pip && pip install -r /app/dockers/chopchop_allen_2018/requirements.txt

WORKDIR /app/dockers/chopchop_allen_2018/indel_prediction
RUN pip install .
WORKDIR /app/dockers/chopchop_allen_2018/selftarget_pyutils
RUN pip install .

ENV INDELGENTARGET_EXE /usr/local/bin/indelgentarget
COPY dockers/Cas9Emulation.py /app
ENV PYTHONPATH /app

ENTRYPOINT ["python", "/app/dockers/chopchop_allen_2018/run_forecast_prediction.py"]
