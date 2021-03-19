FROM python:3.9-slim-buster

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

WORKDIR /sfms
RUN ls -l

COPY . .
RUN chmod 744 .

EXPOSE 8001

CMD ["python", app.py]