FROM python:3.6

EXPOSE 5000
ENV FLASK_APP app.py

COPY ./requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /app

COPY . /app/
CMD ["flask", "run", "--host=0.0.0.0"]
