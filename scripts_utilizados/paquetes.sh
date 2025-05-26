#!/bin/bash
set -ex
sudo apt update
sudo add-apt-repository ppa:ubuntuhandbook1/ppa

## Installing Ubuntu APT packages (required sudo privileges)
sudo apt-get install -y --no-install-recommends \
      "build-essential" \
      "m4" \
      "make" \
      "pkg-config" \
      "unzip" \
      "zip" \
      "git" \
      "wget" \
      "cmake" \
      "gcc" \
      "libcgal-dev" \
      "libgmp-dev" \
      "libgsl-dev" \
      "libcfitsio-dev" \
      "libmgl-dev" \
      "mathgl" \
      "libsdl-image1.2-dev" \
      "qtchooser" \

     "libcgal-qt5-dev" \
     "qt4-bin-dbg" \
     "qt4-dev-tools"
sudo apt-get install freeglut3-dev libgif-dev libfltk1.3-dev swig
sudo apt-get install libwxgtk3.0-gtk3-dev
sudo apt-get install qt4-dev-tools libqt4-dev libqt4-opengl-dev

sudo apt-get install qt4-default
sudo pip install astropy

#sudo apt-get install libqt5core5a libqt5gui5
#sudo apt-get install qt5-qmake
#sudo apt-get install qt5-default
