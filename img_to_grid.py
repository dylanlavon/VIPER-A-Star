from PIL import Image
import argparse
import os
import colors

# Setup args
parser = argparse.ArgumentParser()
parser.add_argument("source_img", type=str, help="Source image name from within the source_images directory.")
parser.add_argument("size", type=int, help="Desired width / height of the square output image.")
parser.add_argument("--binary", type=float, help="For conversions with only barriers and free nodes. Thresholds pixel alpha to 255 or 0 based on this ratio, where values above 255 * bw become opaque and below become transparent.")
args = parser.parse_args()

# Save the new downscaled image
out_image_path = os.path.join("maps", args.source_img + ".out.png")

# Open and downscale the source image
source_image_path = os.path.join("source_images", args.source_img + ".png")
image = Image.open(source_image_path).convert("RGB")
resized_image = image.resize((int(args.size), int(args.size)))

# Convert to barrier/free nodes
if args.binary:
    if args.binary < 0 or args.binary > 1:
        print("ERR: bw ratio out of bounds. Please use a value between 0 and 1.")
        quit()

    # Convert to grayscale for brightness analysis
    resized_image = resized_image.convert("L")  # Convert to grayscale

    # Get pixel access
    bw_image = Image.new("RGB", resized_image.size)  # Create a new blank image
    pixels = bw_image.load()
    gray_pixels = resized_image.load()

    # Process each pixel
    for y in range(resized_image.height):
        for x in range(resized_image.width):
            brightness = gray_pixels[x, y]  # Get grayscale intensity (0-255)
            if brightness < 255 * args.binary:
                pixels[x, y] = colors.BLACK
            else:
                pixels[x, y] = colors.WHITE
    bw_image.save(out_image_path)
    quit()
    
# Save the new downscaled image
resized_image.save(out_image_path)