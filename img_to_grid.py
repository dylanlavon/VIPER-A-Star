from PIL import Image
import argparse
import os
import colors

# Setup args
parser = argparse.ArgumentParser()
parser.add_argument("source_img", type=str, help="Source image name from within the source_images directory.")
parser.add_argument("size", type=int, help="Desired width / height of the square output image.")
parser.add_argument("--binary", type=float, help="For conversions with only barriers and free nodes. Thresholds pixel alpha to 255 or 0 based on this ratio, where values above 255 * bw become opaque and below become transparent.")
parser.add_argument("--fivesplit", type=int, nargs="+", help="For conversions with 4 edge weights and barrier nodes. Use five values from 0-255 to determine the ranges for which between them edge weights are determined.")
args = parser.parse_args()

source_img_stripped = os.path.splitext(args.source_img)[0]

# Save the new downscaled image
out_image_path = os.path.join("maps", source_img_stripped + ".out.png")

# Open the image and check that its square
source_image_path = os.path.join("source_images", args.source_img)
image = Image.open(source_image_path).convert("RGB")
if image.width != image.height:
    print(f"ERR: Source image is not a square.\nWidth: {image.width}\nHeight: {image.height}")

# Scale down the image
resized_image = image.resize((args.size, args.size))

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

if args.fivesplit:
    if len(args.fivesplit) != 5:
        print("ERR: Using fivesplit requires 5 values between 0-255.")
        quit()
    for val in args.fivesplit:
        if val < 0 or val > 255:
            print("ERR: Using fivesplit requires 5 values between 0-255.")
            quit()
    split_points = sorted(args.fivesplit)

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
            if brightness < split_points[0]:
                pixels[x, y] = colors.BLACK
            elif brightness < split_points[1]:
                pixels[x, y] = colors.FIVESPLIT_4
            elif brightness < split_points[2]:
                pixels[x, y] = colors.FIVESPLIT_3
            elif brightness < split_points[3]:
                pixels[x, y] = colors.FIVESPLIT_2
            elif brightness < split_points[4]:
                pixels[x, y] = colors.FIVESPLIT_1
            else:
                pixels[x, y] = colors.WHITE
    bw_image.save(out_image_path)
    quit()
    
# Save the new downscaled image
resized_image.save(out_image_path)