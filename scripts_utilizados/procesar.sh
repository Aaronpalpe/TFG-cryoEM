#!/bin/bash

# Lista de archivos sin la extensión
files=("40-8")

for file in "${files[@]}"; do
    echo "Procesando $file..."
    
    # Convertir JPG a FITS
    python jpg_to_fits.py ./"$file".jpg ./"$file".fits

    # Ejecutar mse con los parámetros indicados
    ./mse "$file".fits -cut 40 -upSkl -mask mascara.png

    # Ejecutar skelconv en el archivo resultante
    ./skelconv "$file".fits_c40.up.NDskl -to vtp

    echo "Finalizado $file"
done

echo "Todos los archivos han sido procesados."
