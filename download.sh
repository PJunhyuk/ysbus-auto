#!/bin/sh

rm -r src
mkdir src
cd src
wget "https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip"
unzip chromedriver_linux64.zip
