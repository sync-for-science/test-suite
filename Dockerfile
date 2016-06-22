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
RUN wget --quiet https://bitbucket.org/ariya/phantomjs/downloads/phantomjs-2.1.1-linux-x86_64.tar.bz2
RUN tar xvfj /opt/phantomjs-2.1.1-linux-x86_64.tar.bz2 && \
    ln -s /opt/phantomjs-2.1.1-linux-x86_64/bin/phantomjs /usr/bin/phantomjs

RUN mkdir /demo-test-suite
WORKDIR /demo-test-suite

# Copy the codebase
COPY requirements.txt /demo-test-suite
# Install requirements
RUN pip install -r requirements.txt

COPY . /demo-test-suite

CMD supervisord -c /demo-test-suite/supervisord.conf
