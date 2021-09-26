#!/bin/bash
python3 clickdelay.py &
echo 'flask app created'
python3 timer1.py &
echo 'timer1 created'
wait