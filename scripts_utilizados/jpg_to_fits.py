import numpy as np
from PIL import Image
import astropy.io.fits as fits
import sys
import os

def jpg_to_fits(entrada, salida):
    # Verificar si los archivos existen
    if not os.path.isfile(entrada):
        print(f"Error: El archivo {entrada} no existe.")
        return

    # Abrir la imagen .jpg y convertirla a escala de grises
    image = Image.open(entrada).convert('L')

    # Corregir la rotación y el volteo horizontal
    image = image.rotate(180).transpose(Image.FLIP_LEFT_RIGHT)

    # Convertir la imagen a una matriz NumPy
    image_data = np.array(image)

    # Crear un objeto FITS PrimaryHDU
    hdu = fits.PrimaryHDU(data=image_data)

    # Escribir el archivo FITS
    hdu.writeto(salida, overwrite=True)

    print("¡Conversión completa!")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python jpg_to_fits.py <input_jpg_file> <output_fits_file>")
    else:
        input_jpg = sys.argv[1]
        output_fits = sys.argv[2]
        jpg_to_fits(input_jpg, output_fits)
