#!/bin/sh

echo "hello"

cmake .. \
	-DCMAKE_BUILD_TYPE=Release \
	-DBLAS="Open" \
	-Dpython_version=3 \
	-DBoost_PYTHON_LIBRARY_RELEASE=/usr/local/opt/boost-python3/lib/libboost_numpy39.dylib \
	-DCMAKE_CXX_FLAGS="-std=c++14"
make -j8
