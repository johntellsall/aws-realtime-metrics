FROM python:3.7

WORKDIR /app
EXPOSE 6543

# install requirements first (faster dev)
COPY requirements.txt /app/
RUN pip install -qr requirements.txt

COPY . /app/
CMD pytest -v && python randocat.py