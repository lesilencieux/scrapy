FROM python:alpine3.6
MAINTAINER Mouhoutassim BELLO (mouhoutassim.bello@rintio.com)
RUN pip install --upgrade pip
COPY . /app
WORKDIR /app
EXPOSE 8585
RUN pip install -r requirements.txt
ENTRYPOINT ["python"]
CMD ["index.py"]