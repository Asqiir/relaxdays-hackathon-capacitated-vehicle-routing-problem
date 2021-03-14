FROM python:3.9
WORKDIR /app
ADD . /app
RUN python3 -m pip install numpy
RUN python3 -m pip install poetry
RUN python3 -m pip install python-tsp
RUN python3 -m pip 
ENV NAME World
ENTRYPOINT ["python3","main.py"]
