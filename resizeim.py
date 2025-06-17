import os
from PIL import Image

# Configuration
folder = 'assets/gallery'
target_size = (300, 300)  # Resize target (width, height)

# Supported image formats
supported_formats = ('.jpg', '.jpeg', '.png', '.webp')

# Loop through all files in the folder
for filename in os.listdir(folder):
    if filename.lower().endswith(supported_formats):
        file_path = os.path.join(folder, filename)

        with Image.open(file_path) as img:
            img = img.convert('RGB')  # Ensure compatibility
            
            width, height = img.size
            min_dim = min(width, height)

            if height > width:
                # Portrait: crop top square
                left = 0
                top = 0
                right = min_dim
                bottom = min_dim
            else:
                # Landscape or square: center crop
                left = (width - min_dim) // 2
                top = (height - min_dim) // 2
                right = left + min_dim
                bottom = top + min_dim

            img = img.crop((left, top, right, bottom))
            
            # Resize to target size
            img = img.resize(target_size, Image.Resampling.LANCZOS)
            
            img.save(file_path, format='JPEG', quality=85)  # Overwrite original file

        print(f"Resized and cropped {filename} in place.")

print("Batch resizing and cropping complete!")
