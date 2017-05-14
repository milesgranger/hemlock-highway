FROM ubuntu:16.04

RUN apt update \
    && apt upgrade -y \
    && apt install -y htop iputils-ping vim build-essential wget unzip nginx ufw \
    && apt install -y aptitude dialog net-tools tcl8.5 git

# Turn off daemon mode
# Reference: http://stackoverflow.com/questions/18861300/how-to-run-nginx-within-docker-container-without-halting
RUN echo "\ndaemon off;" >> /etc/nginx/nginx.conf
RUN cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.original

# Install python stuff
RUN wget https://repo.continuum.io/miniconda/Miniconda3-4.2.12-Linux-x86_64.sh -O miniconda.sh
RUN bash miniconda.sh -bf -p /anaconda
ENV PATH /anaconda/bin:$PATH
RUN conda config --add channels numbda
RUN conda config --add channels conda-forge
RUN pip install --upgrade pip
RUN pip install s3fs sqlalchemy psycopg2 boto3 flask bokeh uwsgi pynamodb
RUN pip install redis Flask-Dance Flask-WTF

WORKDIR /workdir

EXPOSE 5555
EXPOSE 80
EXPOSE 443
