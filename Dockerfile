FROM python:3.6

RUN mkdir -p /app
WORKDIR /app
EXPOSE 8080

# install requirements first (faster dev)
COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY . /app/

CMD ["python", "./randocat.py"]
