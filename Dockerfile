FROM python:3.11

WORKDIR /app

COPY requriements.txt .

RUN python3 -m pip install --upgrade pip
RUN python3 -m pip install -r requriements.txt

COPY *.py server.log /app
COPY templates /app/templates
COPY static /app/static

RUN python3 data_generation.py && \
    python3 train1_for_category.py && \
    python3 train2_for_severity.py && \
    python3 train3_for_rootcause.py && \
    python3 predict_result.py

EXPOSE 7008
CMD ["gunicorn", "--preload", "-w", "2", "-k", "gthread", "--threads", "4", "-b", "0.0.0.0:7008", "wsgi:app"]
