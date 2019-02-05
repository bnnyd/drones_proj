#!/usr/csh

rm -f no_obj*
rm -f too_many*

python3 imageProcessing.py
python3 OfflineVideo.py
