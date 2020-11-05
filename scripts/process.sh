#!/bin/bash

function get_px_size() {
    local px=$(echo $1 | grep Pixel)
    echo px
}

wget -i downloadlist.txt
unzip \*.zip

OUTPUT_FILE=mega_w2
PRECISION=0.5
EXTENSION=.img
FILES=( "*.img *.tif" )
px_tmp = $(gdalinfo "${FILES[0]}" | grep Pixel)
PX_SIZE=

# sudo apt install gdal python-gdal build-essential cmake libboost-all-dev libgdal-dev
gdal_merge.py -o mega_tile.tif -of GTiff -ot Float32 -v -ps $PX_SIZE $PS_SIZE *.img *.tif
# git clone https://github.com/heremaps/tin-terrain.git
# cd tin-terrain
./tin-terrain dem2tin --input mega_tile.tif --output $OUTPUT_FILE.obj --method zemlya --max-error $PRECISION
# pip install meshio
meshio-convert $OUTPUT_FILE.obj $OUTPUT_FILE.ply
