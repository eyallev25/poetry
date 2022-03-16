# syntax=docker/dockerfile:1.0.0-experimental

FROM python:3.9

WORKDIR /anun-tracer-benchmark

# install poetry
RUN pip3 install poetry

# copy dirs
COPY scripts scripts
COPY tests tests
RUN mkdir outputs

# change working directory to tests
WORKDIR /anun-tracer-benchmark/tests

# install tests deps
RUN poetry install

# change working directory to the scripts dir
WORKDIR /anun-tracer-benchmark/scripts




