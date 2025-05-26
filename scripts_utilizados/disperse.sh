#!/bin/bash

set -ex

mkdir disperse
cd disperse

# Install latest DisPerSe from source
wget --no-check-certificate https://github.com/thierry-sousbie/DisPerSE/archive/refs/heads/master.tar.gz
tar -xf master.tar.gz
rm -rf master.tar.gz

# Install mgl
cd DisPerSE-master/external
tar -xf mathgl-1.11.3-2.tar.gz
cd mathgl-1.11.3-2
sudo chmod 777 *


# Si mgl da problemas en la instalacion, sustituir en mgl/mgl_fit.cpp:
# gsl_multifit_covar(s->J, 0.0, covar);
# POR
# // Crear una matriz para almacenar la Jacobiana
# gsl_matrix *J = gsl_matrix_alloc(n, m);
# // Obtener la Jacobiana
# gsl_multifit_fdfsolver_jac(s, J);
# // Calcular la matriz de covarianza con J
# gsl_multifit_covar(J, 0.0, covar);

sudo cmake .
sudo cmake .
sudo make

sudo ./configure --enable-qt
sudo make #-j$(nproc)
sudo make install

# Compile
cd ../../src/
sudo cmake ../ -DMATHGL_DIR=../external/mathgl-1.11.3-2/ -DMATHGL_DIR_INCLUDE=../external/mathgl-1.11.3-2/include

sudo make
sudo make install
export LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
