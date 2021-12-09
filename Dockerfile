FROM      python:slim-buster
RUN       pip install requests
WORKDIR   /app
COPY      main.py main.py
CMD       ["python", "main.py"]
