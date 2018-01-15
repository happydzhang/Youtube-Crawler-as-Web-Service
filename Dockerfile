FROM selenium/standalone-chrome

MAINTAINER Daniel Zhang

USER root

RUN wget https://bootstrap.pypa.io/get-pip.py
RUN python3 get-pip.py
RUN python3 -m pip install selenium
RUN apt-get update && apt-get install -y git
RUN pip install Flask
RUN git clone https://github.com/happydzhang/Youtube-Crawler-as-Web-Service.git


# Bundle app source
COPY webserver.py /src/webserver.py
COPY chromedriver /src/chromedriver
COPY collectData.py /src/collectData.py
COPY pipeline.py /src/pipeline.py

EXPOSE  5000
CMD ["python3", "/src/webserver.py", "-p 5000"]


#docker build . -t selenium-chrome && \
    #docker run -it selenium-chrome python3
