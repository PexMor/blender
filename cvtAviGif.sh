#!/bin/bash

INPUT=output0001-0060.avi

cd render
ffmpeg -i $INPUT -vf "fps=10,scale=640:-1:flags=lanczos" -c:v pam -f image2pipe - | \
    convert -delay 15 - -loop 0 -layers optimize output.gif
