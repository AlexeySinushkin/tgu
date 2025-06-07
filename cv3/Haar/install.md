https://stackoverflow.com/questions/36862589/install-opencv-in-a-docker-container



wget --output-document cv.zip https://github.com/opencv/opencv/archive/3.4.0.zip
wget --output-document contrib.zip https://github.com/opencv/opencv_contrib/archive/3.4.0.zip
unzip cv.zip
unzip contrib.zip
cd opencv-3.4.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.0/modules \
  -D BUILD_opencv_apps=ON \
  -D BUILD_opencv_createsamples=ON \
  -D OPENCV_ENABLE_NONFREE=ON \
  -D CMAKE_CXX_STANDARD=11 \
  -D CMAKE_CXX_FLAGS="-Wno-error=nonnull-compare" \
  -D CMAKE_C_FLAGS="-Wno-error=nonnull-compare" \
  -D CMAKE_C_COMPILER=/usr/bin/gcc-10 \
  -D CMAKE_CXX_COMPILER=/usr/bin/g++-10 \
  ..
make -j 8
make install 
ldconfig

find negatives -name '*.jpg' > negatives.txt
./opencv_createsamples -info positives.txt -num 30 -w 24 -h 24 -vec positives.vec
mkdir cascade_output
./opencv_traincascade -data cascade_output -vec positives.vec -bg negatives.txt -numPos 24 -numNeg 30 -numStages 10 -w 24 -h 24