FROM ubuntu:16.04

RUN apt update \
    && apt upgrade -y \
    && apt install -y htop iputils-ping vim build-essential wget unzip \
    && apt install -y dialog net-tools git

# Install python stuff
RUN wget https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh -O miniconda.sh
RUN bash miniconda.sh -bf -p /anaconda
ENV PATH /anaconda/bin:$PATH
RUN conda config --add channels numba
RUN conda config --add channels conda-forge
RUN pip install --upgrade pip
RUN conda install scikit-learn numpy pandas -y
RUN pip install msgpack-python redis

WORKDIR /workdir

