FROM python:3.9-slim-buster

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /sfms

EXPOSE 8001

COPY . .
RUN chmod 744 .

CMD ["python", "app.py"]