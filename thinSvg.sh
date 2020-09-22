#!/bin/bash

BN=`printf "render/output%04d-%04d" 1 60`
IFN="${BN}.svg"
OFN="${BN}-x.svg"
sed 's/stroke-width="3.0"/stroke-width="0.5"/' <$IFN >$OFN
