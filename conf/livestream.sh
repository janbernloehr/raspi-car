#!/bin/bash

LD_LIBRARY_PATH=/home/pi/raspi-car/mjpg-streamer/ /home/pi/raspi-car/mjpg-streamer/mjpg_streamer -i "input_uvc.so -r 320x240 -f 15 -n -y" -o "output_http.so -p 8071 -w /home/pi/raspi-car/mjpg-streamer/www"
