import disperse_io as di
import numpy as np
import vtk
import matplotlib.pyplot as plt
from PIL import Image
from skimage.morphology import dilation, square, skeletonize
from cldice_metric.cldice import cl_score, clDice

# Global variable to select the sample
SAMPLE_ID = 1  # Set to 1 or 2 to select the sample

# Configuration for samples
SAMPLE_CONFIG = {
    1: {
        "vtp_file": "40-8.fits_c45.4.up.NDskl.vtp",
        "manual_png": "manual.png",
        "cryo_png": "cryo.png",
        "base_image": "cel1.jpg"
    },
    2: {
        "vtp_file": "matriz40-10.fits_c45.up.NDskl.vtp",
        "manual_png": "manual2.png",
        "cryo_png": "cryo2.png",
        "base_image": "cel2.jpg"
    }
}

def leer_png(nombre_archivo):
    """Read a PNG image and convert it to a binary array."""
    imagen = Image.open(nombre_archivo).convert("L")
    return (np.array(imagen) < 128).astype(int)

def leer_vtp(nombre_archivo, size=(1024, 1024, 1)):
    """Read a VTP file and convert it to a rotated NumPy array."""
    reader = vtk.vtkXMLPolyDataReader()
    reader.SetFileName(nombre_archivo)
    reader.Update()
    poly_data = reader.GetOutput()
    return np.logical_not(np.logical_not(np.squeeze(np.rot90(di.vtp_to_numpy(poly_data, size=size)))))

def dilate_image(image, size=15):
    """Dilate a binary image using a square structuring element."""
    return dilation(image, square(size))

def convertir_a_rgb(binaria, color):
    """Convert a binary image to RGB with the specified color."""
    rgb = np.zeros((*binaria.shape, 3), dtype=np.uint8)
    rgb[binaria == 1] = color
    return rgb

def superponer_imagenes(base, overlay):
    """Superpose two RGB images and ensure valid pixel values."""
    return np.clip(base + overlay, 0, 255)

def superponer_imagenes2(base, overlay):
    """Superpose two RGB images, prioritizing non-zero pixels from overlay."""
    result = base.copy()
    mask = np.any(overlay > 0, axis=2)
    result[mask] = overlay[mask]
    return result

def calculate_metrics(predicted, predicted2, ground_truth, dilation_sizes=range(1, 31, 2)):
    """Calculate clDice, Tprec, and Tsens metrics for different dilation sizes."""
    tprec_disperse, tsens_disperse, cldice_disperse = [], [], []
    tprec_cryosparc, tsens_cryosparc, cldice_cryosparc = [], [], []

    for size in dilation_sizes:
        # Dilate images
        pred_dilate = dilate_image(predicted, size)
        pred2_dilate = dilate_image(predicted2, size)
        gt_dilate = dilate_image(ground_truth, size)

        # Metrics for DisPerSE
        tprec_disperse.append(cl_score(pred_dilate, skeletonize(gt_dilate)))
        tsens_disperse.append(cl_score(gt_dilate, skeletonize(pred_dilate)))
        cldice_disperse.append(clDice(pred_dilate, gt_dilate))

        # Metrics for CryoSPARC
        tprec_cryosparc.append(cl_score(pred2_dilate, skeletonize(gt_dilate)))
        tsens_cryosparc.append(cl_score(gt_dilate, skeletonize(pred2_dilate)))
        cldice_cryosparc.append(clDice(pred2_dilate, gt_dilate))

    return (tprec_disperse, tsens_disperse, cldice_disperse,
            tprec_cryosparc, tsens_cryosparc, cldice_cryosparc)

def plot_metrics(dilation_sizes, tprec_disperse, tsens_disperse, cldice_disperse,
                 tprec_cryosparc, tsens_cryosparc, cldice_cryosparc):
    """Plot Tprec, Tsens, and clDice metrics for DisPerSE and CryoSPARC."""
    fig, axes = plt.subplots(3, 1, figsize=(8, 8))

    # Tprec plot
    axes[0].plot(dilation_sizes, tprec_disperse, label='DisPerSE', marker='o')
    axes[0].plot(dilation_sizes, tprec_cryosparc, label='CryoSPARC', marker='s')
    axes[0].set_title('Tprec vs Dilation Size')
    axes[0].set_xlabel('Dilation Size')
    axes[0].set_ylabel('Tprec')
    axes[0].legend()
    axes[0].grid(True)

    # Tsens plot
    axes[1].plot(dilation_sizes, tsens_disperse, label='DisPerSE', marker='o')
    axes[1].plot(dilation_sizes, tsens_cryosparc, label='CryoSPARC', marker='s')
    axes[1].set_title('Tsens vs Dilation Size')
    axes[1].set_xlabel('Dilation Size')
    axes[1].set_ylabel('Tsens')
    axes[1].legend()
    axes[1].grid(True)

    # clDice plot
    axes[2].plot(dilation_sizes, cldice_disperse, label='DisPerSE', marker='o')
    axes[2].plot(dilation_sizes, cldice_cryosparc, label='CryoSPARC', marker='s')
    axes[2].set_title('clDice vs Dilation Size')
    axes[2].set_xlabel('Dilation Size')
    axes[2].set_ylabel('clDice')
    axes[2].legend()
    axes[2].grid(True)

    plt.tight_layout()
    plt.subplots_adjust(hspace=0.4)
    plt.show()

def plot_images(base_image_path, ground_truth, predicted, predicted2, superimposed, superimposed2):
    """Display original, ground truth, predicted, and superimposed images."""
    fig, axes = plt.subplots(3, 2, figsize=(6, 8))
    imagenes = [
        (base_image_path, "Imagen PNG"),
        (ground_truth, "Ground Truth"),
        (predicted, "Esqueleto DisPerSE"),
        (predicted2, "Esqueleto CryoSPARC"),
        (superimposed, "Superpuesto DisPerSE"),
        (superimposed2, "Superpuesto CryoSPARC")
    ]

    for ax, (img, title) in zip(axes.flat, imagenes):
        if title in ["Ground Truth", "Esqueleto DisPerSE", "Esqueleto CryoSPARC"]:
            ax.imshow(img, cmap="binary")
        else:
            ax.imshow(Image.open(img) if isinstance(img, str) else img, cmap="gray" if isinstance(img, str) else None)
        ax.set_title(title)
        ax.axis("off")

    plt.tight_layout()
    plt.show()

def main():
    """Main function to execute the image processing and analysis pipeline."""
    # Load sample configuration
    config = SAMPLE_CONFIG[SAMPLE_ID]

    # Load images
    predicted = leer_vtp(config["vtp_file"])
    predicted2 = leer_png(config["cryo_png"])
    ground_truth = leer_png(config["manual_png"])

    # Calculate metrics
    dilation_sizes = range(1, 31, 2)
    metrics = calculate_metrics(predicted, predicted2, ground_truth, dilation_sizes)
    tprec_disperse, tsens_disperse, cldice_disperse, tprec_cryosparc, tsens_cryosparc, cldice_cryosparc = metrics

    # Plot metrics
    plot_metrics(dilation_sizes, tprec_disperse, tsens_disperse, cldice_disperse,
                 tprec_cryosparc, tsens_cryosparc, cldice_cryosparc)

    # Convert to RGB for visualization
    ground_truth_rgb = convertir_a_rgb(dilate_image(ground_truth), [255, 0, 0])  # Red
    predicted_rgb = convertir_a_rgb(dilate_image(predicted), [0, 255, 0])  # Green
    predicted2_rgb = convertir_a_rgb(dilate_image(predicted2), [0, 255, 0])  # Green

    # Superimpose images
    superimposed = superponer_imagenes(ground_truth_rgb, predicted_rgb)
    superimposed2 = superponer_imagenes(ground_truth_rgb, predicted2_rgb)

    # Plot images
    plot_images(config["base_image"], ground_truth, predicted, predicted2, superimposed, superimposed2)

    # Print clDice values
    print(f"El valor de clDice con DisPerSE (dilatación 15) es: {clDice(dilate_image(predicted), dilate_image(ground_truth))}")
    print(f"El valor de clDice con CryoSPARC (dilatación 15) es: {clDice(dilate_image(predicted2), dilate_image(ground_truth))}")

    # Superimpose base image with predictions
    base_image = np.array(Image.open(config["base_image"]).convert("RGB").resize((1024, 1024)))
    superimposed_vtp = superponer_imagenes2(base_image, predicted_rgb)
    superimposed_png = superponer_imagenes2(base_image, predicted2_rgb)

    # Display superimposed images
    plt.figure(figsize=(6, 6))
    plt.imshow(superimposed_vtp)
    plt.title(f"{config['base_image']} superpuesta con {config['vtp_file']}")
    plt.axis("off")
    plt.show()

    plt.figure(figsize=(6, 6))
    plt.imshow(superimposed_png)
    plt.title(f"{config['base_image']} superpuesta con {config['cryo_png']}")
    plt.axis("off")
    plt.show()

if __name__ == "__main__":
    main()
