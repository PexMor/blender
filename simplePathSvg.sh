#!/bin/bash

BN=`printf "render/output%04d-%04d" 1 60`
IFN="${BN}.svg"
OFN="${BN}-x.svg"
SFN="${BN}-s.svgz"

echo "remove attributes (otherwise scour fails)"
sed 's#^\([[:space:]]*<path d="\)[[:space:]]*\([^"]*[^[:space:]]\)[[:space:]]*".*$#\1\2" />#g' <$IFN >$OFN
echo "clean paths"
scour -i $OFN -o $SFN --enable-viewboxing --enable-id-stripping \
  --enable-comment-stripping --shorten-ids --indent=none

