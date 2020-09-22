#!/bin/bash

vlc() {
    /Applications/VLC.app/Contents/MacOS/VLC "$@"
}

vlc render/output0001-0060.avi --loop --video-on-top