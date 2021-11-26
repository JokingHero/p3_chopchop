FROM python:2.7

#COPY dockers/Cas9Emulation.py .

WORKDIR /chopchop_inDelphi

RUN pip install --upgrade pip \
 && pip install scikit-learn==0.18.1 numpy pandas scipy

# Add script
ADD . .
COPY dockers/Cas9Emulation.py .
ENV PYTHONPATH .

ENTRYPOINT ["python", "./dockers/chopchop_indelphi/run_repair_prediction.py"]