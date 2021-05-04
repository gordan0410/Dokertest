FROM python:3.7
RUN mkdir /code
ENV PYTHONUNBUFFERED 1
WORKDIR /code
RUN python3 -m pip install -U pip
COPY pip_requirements.txt /code
RUN pip install -r pip_requirements.txt
COPY ./ /code