import os
from PIL import Image

# Define the folder containing the images
input_folder = r"C:\Users\swara\OneDrive\Desktop\images"  # Update with your folder path

# Loop through all the files in the folder
for file_name in os.listdir(input_folder):
    # Create the full file path
    file_path = os.path.join(input_folder, file_name)

    # Only process image files (you can add more extensions if needed)
    if file_name.lower().endswith(('.png', '.jpeg', '.bmp', '.gif', '.tiff')):
        try:
            # Open the image
            with Image.open(file_path) as img:
                # Convert the image to RGB (required for saving as JPG)
                rgb_image = img.convert('RGB')

                # Define the new file name with the .jpg extension
                output_path = os.path.splitext(file_path)[0] + '.jpg'

                # Save the image in JPG format (overwrite original image)
                rgb_image.save(output_path, 'JPEG')
                print(f"Converted {file_name} to JPG.")
                
                # Optionally, you can remove the original file if needed:
                # os.remove(file_path)  # Uncomment to delete original files after conversion
                
        except Exception as e:
            print(f"Error processing {file_name}: {e}")
