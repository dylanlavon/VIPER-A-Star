from PIL import Image
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("source_img", help="Source image name from within the source_images directory.")
parser.add_argument("size", help="Desired width / height of the square output image.")
args = parser.parse_args()

# Open and downscale the source image
source_image_path = os.path.join("source_images", args.source_img + ".png")
image = Image.open(source_image_path).convert("RGBA")
resized_image = image.resize((int(args.size), int(args.size)))

# Save the new 50x50 image
out_image_path = os.path.join("output_images", args.source_img + ".out.png")
resized_image.save(out_image_path)