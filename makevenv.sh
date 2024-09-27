#!/bin/bash


rm -rf .venv

python3 -m venv .venv


.venv/bin/pip3 install -r requirements.txt

cp secrets.py.example secrets.py
