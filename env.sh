#!/bin/bash

sudo apt-get clean
sudo apt-get update -q --fix-missing

export LANG=C.UTF-8 LC_ALL=C.UTF-8
export PYTHONIOENCODING UTF-8
export PATH /home/conda/bin:$PATH

cd ~/
sudo apt-get install -y wget apt-utils nano bzip2 ca-certificates libglib2.0-0 libxext6 libsm6 libxrender1 git
sudo wget --quiet https://repo.anaconda.com/archive/Anaconda3-5.2.0-Linux-x86_64.sh -O ~/anaconda.sh && \
    /bin/bash ~/anaconda.sh -b -p /home/conda && \
    rm ~/anaconda.sh && \
    ln -s /home/conda/etc/profile.d/conda.sh /etc/profile.d/conda.sh && \
    echo ". /home/conda/etc/profile.d/conda.sh" >> ~/.bashrc && echo "conda activate base" >> ~/.bashrc

sudo apt-get install -y curl grep sed dpkg && \
    TINI_VERSION=`curl https://github.com/krallin/tini/releases/latest | grep -o "/v.*\"" | sed 's:^..\(.*\).$:\1:'` && \
    curl -L "https://github.com/krallin/tini/releases/download/v${TINI_VERSION}/tini_${TINI_VERSION}.deb" > tini.deb && \
    dpkg -i tini.deb && \
    rm tini.deb && \
    apt-get clean
sudo apt-get install make gcc wget git ca-certificates -y
wget https://storage.googleapis.com/golang/go1.10.3.linux-amd64.tar.gz
sudo tar -C /usr/bin -xzf go1.10.3.linux-amd64.tar.gz
export PATH=$PATH:/usr/bin/go/bin
export GOROOT=/usr/bin/go
sudo mkdir /home/go
export GOPATH=/home/go

sudo apt-get -qy autoremove

conda create --name blueblood python
source activate blueblood
conda install numpy scipy pandas numba cython lxml tensorflow pymc3 scikit-learn -y
conda install -c conda-forge fastparquet -y
conda install -c conda-forge hdbscan
pip install -r requirements.txt
cd app/models
pip install -r requirements.txt
python -m nltk.downloader all
source deactivate
go get -u github.com/alpacahq/marketstore
cd $GOPATH/src/github.com/alpacahq/marketstore
make configure
make install
make install
go get github.com/quickfixgo/quickfix
