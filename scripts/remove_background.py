import argparse
from PIL import Image
import numpy as np


def process_image(image_path):
    # Load the image
    img = Image.open(image_path)
    # Convert the image to RGB if it's not already
    img_rgb = img.convert("RGB")

    # Convert the image to a numpy array
    img_np = np.array(img_rgb)

    # Extract RGB values
    r, g, b = img_np[:, :, 0], img_np[:, :, 1], img_np[:, :, 2]

    # Find the median color
    median_color = np.array([np.median(r), np.median(g), np.median(b)])

    # Divide the entire image by the median color
    # To prevent division by zero, add a small epsilon to the median color.
    epsilon = 1e-6
    median_color = np.where(median_color == 0, epsilon, median_color)
    adjusted_img_np = img_np / (median_color / 256)

    # Clip values to the range [0, 255] and convert to uint8
    adjusted_img_np = np.clip(adjusted_img_np, 0, 255).astype(np.uint8)

    # Convert back to an image
    adjusted_img = Image.fromarray(adjusted_img_np)
    adjusted_img.save("no_bg_" + image_path)


def main():
    parser = argparse.ArgumentParser(description="Process images")
    parser.add_argument(
        "image_paths", type=str, nargs="+", help="Paths to the image files"
    )

    args = parser.parse_args()

    for image_path in args.image_paths:
        process_image(image_path)


if __name__ == "__main__":
    main()
