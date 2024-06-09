#!/bin/bash

docker stop pcc-rent
docker rm pcc-rent
docker rmi pcc-rent
docker volume remove pcc-rent