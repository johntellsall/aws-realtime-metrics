FROM python:3.6

WORKDIR /app
EXPOSE 8080

# install requirements first (faster dev)
COPY requirements.txt /app/
RUN pip install -qr requirements.txt
