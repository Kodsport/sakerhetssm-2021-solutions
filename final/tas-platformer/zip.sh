#!/bin/bash

mkdir chall 
cp -r src/game chall/game
cp -r src/images chall/images
cp src/play_interactive.py chall/play_interactive.py
cp src/play_replay.py chall/play_replay.py
cp src/requirements.txt chall/requirements.txt
zip -r chall.zip chall
rm -rf chall