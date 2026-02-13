#!/bin/bash

DATA=$(date +"%Y-%m-%d")

git add .
git commit -m "Progresso do dia $DATA"
git push
