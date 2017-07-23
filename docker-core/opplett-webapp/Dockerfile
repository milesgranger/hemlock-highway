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
RUN pip install s3fs sqlalchemy psycopg2 boto3 flask bokeh uwsgi pynamodb
RUN pip install redis Flask-Dance Flask-WTF stripe uwsgi peewee
RUN pip install msgpack-python python-socketio flask-socketio
RUN conda install bcrypt pandas numpy -y
RUN pip install --upgrade google-api-python-client

# Install frontend stuff
RUN apt install nodejs npm -y
RUN ln -s /usr/bin/nodejs /usr/bin/node
ENV PATH $PATH:/usr/bin
RUN ldconfig -v

WORKDIR /workdir

COPY ./package.json ./
RUN npm install --save --save-dev

