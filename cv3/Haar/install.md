https://stackoverflow.com/questions/36862589/install-opencv-in-a-docker-container

apt install -y libtiff5-dev libjpeg8-dev libpng-dev cmake make
apt install -y libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev
apt install -y libxine2-dev libv4l-dev
apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
apt install -y qt5-default
apt install -y libatlas-base-dev
apt install -y libfaac-dev libmp3lame-dev libtheora-dev
apt install -y libvorbis-dev libxvidcore-dev
apt install -y libopencore-amrnb-dev libopencore-amrwb-dev
apt install -y x264 x265 v4l-utils
apt install -y libprotobuf-dev protobuf-compiler
apt install -y libeigen3-dev

wget --output-document cv.zip https://github.com/opencv/opencv/archive/4.11.0.zip
wget --output-document contrib.zip https://github.com/opencv/opencv_contrib/archive/4.11.0.zip
unzip cv.zip
unzip contrib.zip
cd opencv-4.11.0
mkdir build
cd build
cmake -D CMAKE_BUILD_TYPE=RELEASE \
  -D CMAKE_INSTALL_PREFIX=/usr/local \
  -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-4.11.0/modules \
  -D BUILD_opencv_apps=ON \
  -D OPENCV_ENABLE_NONFREE=ON \
  ..
make -j 8
make install 
ldconfig
/usr/local/share/opencv4/haarcascades/haarcascade_license_plate_rus_16stages.xml

https://www.youtube.com/watch?v=XrCAvs9AePM
