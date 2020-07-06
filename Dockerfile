FROM python:alpine3.6
MAINTAINER Hilaire Ahotonnagnon (hilaireahotonnagnon@gmail.com)
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
EXPOSE 8385
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["index.py"]