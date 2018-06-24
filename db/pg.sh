#!/bin/bash

sudo docker run --name pg -p 5432:5432 \
    -e POSTGRES_PASSWORD=secretpassword \
    -d postgres
