#!/bin/bash

docker run -d -it -p 5432:5432 --name=database -d postgres
