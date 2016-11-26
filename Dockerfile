FROM ubuntu:14.04

MAINTAINER sriram spectacle

# Update packages
RUN apt-get update -y

# Install Python Setuptools
RUN apt-get install -y \
    make \
    build-essential \
    python-pip \
    python-dev \
    libmysqlclient-dev \
    libxml2-dev \
    libxslt1-dev \
    python-lxml \
    libtiff5-dev libjpeg8-dev zlib1g-dev libfreetype6-dev liblcms2-dev libwebp-dev \
    tcl8.6-dev tk8.6-dev python-tk \
;

# Install pip
RUN easy_install pip

# Add and install Python modules
ADD requirements.txt /src/requirements.txt
RUN cd /src; pip install -r requirements.txt

# Bundle app source
ADD . /src
WORKDIR /src

# Expose
EXPOSE  5000

# Run
CMD ["python", "/src/main.py"]
