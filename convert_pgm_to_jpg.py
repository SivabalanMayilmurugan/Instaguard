import os
import cv2  # OpenCV library for image processing
import sys

# ================= CONFIGURATION =================
# Folder containing your original PGM files (BOSSBase)
INPUT_FOLDER = "BOSSBase_1.01" 

# Folder where the new JPEG files will be saved
OUTPUT_FOLDER = "BOSSBase_JPEG_Cover" 

# JPEG Quality Factor (0-100)
# 100 = Best quality (least compression)
# 75 = Standard Social Media/Web quality (Recommended for your project)
JPEG_QUALITY = 75 
# =================================================

def convert_images():
    # 1. Check if input folder exists
    if not os.path.exists(INPUT_FOLDER):
        print(f"Error: Input folder '{INPUT_FOLDER}' not found!")
        print("Please place your PGM images in this folder or update the script.")
        return

    # 2. Create output folder if it doesn't exist
    if not os.path.exists(OUTPUT_FOLDER):
        os.makedirs(OUTPUT_FOLDER)
        print(f"Created output folder: {OUTPUT_FOLDER}")

    # 3. Get list of files
    files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith('.pgm')]
    total_files = len(files)
    
    print(f"Found {total_files} PGM images. Starting conversion...")

    # 4. Loop through and convert
    count = 0
    for filename in files:
        try:
            # Construct full file paths
            input_path = os.path.join(INPUT_FOLDER, filename)
            
            # Create new filename (e.g., 1013.pgm -> 1013.jpg)
            new_filename = os.path.splitext(filename)[0] + ".jpg"
            output_path = os.path.join(OUTPUT_FOLDER, new_filename)

            # Read the PGM image (Flag 0 reads as Grayscale, 1 reads as Color)
            # BOSSBase is usually grayscale.
            img = cv2.imread(input_path, cv2.IMREAD_UNCHANGED)

            if img is None:
                print(f"Warning: Could not read {filename}. Skipping.")
                continue

            # Write the image as JPEG with specific quality
            # [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY] sets the compression level
            cv2.imwrite(output_path, img, [int(cv2.IMWRITE_JPEG_QUALITY), JPEG_QUALITY])
            
            count += 1
            
            # Print progress every 1000 images
            if count % 1000 == 0:
                print(f"Converted {count}/{total_files} images...")

        except Exception as e:
            print(f"Error converting {filename}: {e}")

    print(f"\nSuccess! Converted {count} images.")
    print(f"Saved to folder: {OUTPUT_FOLDER}/")

if __name__ == "__main__":
    convert_images()