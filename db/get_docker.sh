#!/bin/bash

sudo apt-get remove docker docker-engine docker.io -y
sudo apt-get update
sudo apt-get install  apt-transport-https ca-certificates curl software-properties-common -y
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
sudo apt-key fingerprint 0EBFCD88
sudo add-apt-repository \
   "deb [arch=amd64] https://download.docker.com/linux/ubuntu \
   $(lsb_release -cs) \
   stable"
sudo apt-get update
sudo apt-get install docker-ce -y
sudo groupadd docker
sudo usermod -aG docker $USER
sudo systemctl enable docker
