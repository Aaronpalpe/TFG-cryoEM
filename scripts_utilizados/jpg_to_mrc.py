import sys
import mrcfile
import numpy as np
from PIL import Image

def jpg_to_mrc(jpg_path, mrc_path):
    # Cargar la imagen JPG y convertirla a escala de grises
    img = Image.open(jpg_path).convert("L")
    
    # Convertir la imagen a un array de NumPy (float32 para mayor precisión)
    img_array = np.array(img, dtype=np.float32)
    
    # Guardar en formato MRC
    with mrcfile.new(mrc_path, overwrite=True) as mrc:
        mrc.set_data(img_array)

    print(f"Conversión completa: {mrc_path}")

# Ejemplo de uso
if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python jpg_to_fits.py <input_jpg_file> <output_fits_file>")
    else:
        input_jpg = sys.argv[1]
        output_fits = sys.argv[2]
        jpg_to_mrc(input_jpg, output_fits)

#pip install mrcfile pillow numpy
