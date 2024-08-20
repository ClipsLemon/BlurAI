#!bin/bash

rm -fr blurAI.db
rm -fr in_predictions/*
rm -fr out_predictions/*
touch blurAI.db
python script.py
