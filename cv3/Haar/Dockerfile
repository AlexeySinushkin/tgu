# Use an Ubuntu base image, a version that's compatible with GCC-10.
# Ubuntu 20.04 (Focal Fossa) typically comes with GCC-9 by default but supports GCC-10.
# We'll explicitly install GCC-10 and G++-10.
FROM ubuntu:20.04

# Set environment variables to avoid interactive prompts during apt installations
ENV DEBIAN_FRONTEND=noninteractive

RUN apt update
RUN apt install -y build-essential cmake wget unzip pkg-config
RUN apt install -y libtiff5-dev libjpeg8-dev libpng-dev cmake make
RUN apt install -y libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev
RUN apt install -y libxine2-dev libv4l-dev
RUN apt install -y libgstreamer1.0-dev libgstreamer-plugins-base1.0-dev
RUN apt install -y qt5-default
RUN apt install -y libatlas-base-dev
RUN apt install -y libfaac-dev libmp3lame-dev libtheora-dev
RUN apt install -y libvorbis-dev libxvidcore-dev
RUN apt install -y libopencore-amrnb-dev libopencore-amrwb-dev
RUN apt install -y x264 x265 v4l-utils
RUN apt install -y libprotobuf-dev protobuf-compiler
RUN apt install -y libeigen3-dev
RUN apt install -y gcc-10 g++-10

	

# Set the working directory inside the container
WORKDIR /opt/opencv_build

# Download OpenCV and OpenCV_contrib sources
# Use specific archive URLs for version 3.4.0 to ensure consistency and avoid issues
# with git history/branches changing or being unavailable.
RUN wget -q https://github.com/opencv/opencv/archive/3.4.0.zip -O opencv-3.4.0.zip && \
    wget -q https://github.com/opencv/opencv_contrib/archive/3.4.0.zip -O opencv_contrib-3.4.0.zip && \
    unzip -q opencv-3.4.0.zip && \
    unzip -q opencv_contrib-3.4.0.zip && \
    mv opencv-3.4.0 opencv && \
    mv opencv_contrib-3.4.0 opencv-contrib

# Create a build directory
RUN mkdir opencv/build && \
    cd opencv/build && \
    \
    # Run CMake with the specified flags
    # -D CMAKE_BUILD_TYPE=RELEASE: Optimized release build.
    # -D CMAKE_INSTALL_PREFIX=/usr/local: Standard installation path.
    # -D OPENCV_EXTRA_MODULES_PATH: Points to the contrib modules.
    # -D BUILD_opencv_videoio=OFF: Disable videoio module (as per your previous attempts).
    # -D BUILD_opencv_apps=ON: Ensure applications like createsamples are built.
    # -D OPENCV_ENABLE_NONFREE=ON: Enable non-free algorithms (like SIFT, SURF).
    # -D CMAKE_CXX_STANDARD=11: Force C++11 standard for compatibility with OpenCV 3.4.0.
    # -D CMAKE_C_COMPILER and CMAKE_CXX_COMPILER: Explicitly use GCC-10/G++-10.
    # -D CMAKE_CXX_FLAGS and CMAKE_C_FLAGS: Disable specific warnings as errors.
    cmake -D CMAKE_BUILD_TYPE=RELEASE \
          -D CMAKE_INSTALL_PREFIX=/usr/local \
          -D OPENCV_EXTRA_MODULES_PATH=../../opencv-contrib/modules \
          -D BUILD_opencv_apps=ON \
          -D BUILD_opencv_createsamples=ON \
          -D OPENCV_ENABLE_NONFREE=ON \
          -D CMAKE_CXX_STANDARD=11 \
          -D CMAKE_C_COMPILER=/usr/bin/gcc-10 \
          -D CMAKE_CXX_COMPILER=/usr/bin/g++-10 \
          -D CMAKE_CXX_FLAGS="-Wno-error=nonnull-compare" \
          -D CMAKE_C_FLAGS="-Wno-error=nonnull-compare" \
          ../

# Build and install OpenCV
RUN cd opencv/build && \
    make -j$(nproc) && \
    make install && \
    ldconfig

# Set PATH for OpenCV binaries for future interactive use (optional, for debugging inside container)
ENV PATH="/usr/local/bin:${PATH}"

# Command to run when the container starts (optional)
# This can be set to /bin/bash for interactive shell, or to a test command.
# For now, we'll set it to bash so you can inspect the installation.
CMD ["/bin/bash"]
