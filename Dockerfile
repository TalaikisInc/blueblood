FROM ubuntu:latest
MAINTAINER Tadas Talaikis
LABEL version="1.0"
LABEL description="Anaconda with additional wuantitative module for BlueBlood."

RUN apt-get clean
RUN apt-get update -q --fix-missing

ENV LANG=C.UTF-8 LC_ALL=C.UTF-8
ENV PYTHONIOENCODING UTF-8
ENV PATH /opt/conda/bin:$PATH

RUN apt-get install -y wget \
    apt-utils \
    nano \
    bzip2 \
    ca-certificates \
    libglib2.0-0\
    libxext6\
    libsm6\
    libxrender1 \
    git

RUN wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /opt/conda && \
    rm ~/anaconda.sh && \
    ln -s /opt/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /opt/conda/etc/profile.d/conda.sh" >> ~/.bashrc && \
    echo "conda activate base" >> ~/.bashrc

RUN apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean

RUN apt-get -qy autoremove

RUN conda install tensorflow -y
RUN conda install pymc3 -y
RUN conda install cython -y
RUN conda install lxml -y
RUN conda install scikit-learn -y
RUN pip install -r requirements.txt
RUN python -m nltk.downloader all

ENTRYPOINT [ "/usr/bin/tini", "--" ]
CMD [ "/bin/bash" ]
