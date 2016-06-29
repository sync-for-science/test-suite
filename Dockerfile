FROM python:3
MAINTAINER Josh Mandel

# Install required packages
RUN apt-get update
RUN apt-get install -y \
    xvfb unzip chromium chromium-l10n \
    redis-server \
    supervisor
RUN apt-get clean

WORKDIR /opt

# Install chromedriver
RUN wget --quiet http://chromedriver.storage.googleapis.com/2.22/chromedriver_linux64.zip
RUN unzip /opt/chromedriver_linux64.zip -d /opt/ && \
    ln -s /opt/chromedriver /usr/bin/chromedriver

# Install phantomjs
RUN wget --quiet https://github.com/Medium/phantomjs/releases/download/v2.1.1/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN tar xvfj /opt/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    ln -s /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs


RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app

COPY requirements.txt /usr/src/app/
RUN  pip install --no-cache-dir -r requirements.txt
COPY . /usr/src/app

CMD supervisord -c supervisord.conf
