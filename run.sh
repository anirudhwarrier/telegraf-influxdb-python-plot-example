#!/bin/bash

docker-compose up -d
sleep 10
python3 -m venv myenv
source myenv/bin/activate
pip install -r requirements.txt
python3 plot.py