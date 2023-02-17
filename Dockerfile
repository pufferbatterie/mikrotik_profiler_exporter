FROM python:3.10-alpine

COPY . .

RUN pip install -r requirements.txt

CMD python main.py


# docker build . -t mikrotik_profiler_exporter