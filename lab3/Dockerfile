FROM --platform=linux/amd64 python:alpine

WORKDIR /home/app

COPY ./app/requirements.txt ./
RUN pip install -r requirements.txt --no-cache-dir

COPY ./app ./

ENTRYPOINT ["python" , "-m", "flask", "run"]
CMD ["--port", "8080", "--host", "0.0.0.0"]