import os
import shutil

# Input directory to sort files
From = input("ENTER THE DIRECTORY YOU WANT TO SORT: ")
os.chdir(From)

# File extension categories 
extensions = {
    "images": [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".svg", ".webp"],
    "videos": [".mp4", ".avi", ".mkv", ".mov", ".wmv", ".flv", ".webm", ".mpeg"],
    "pdf": [".pdf"],
    "word": [".doc", ".docx"],
    "excel": [".xls", ".xlsx", ".xlsm"],
    "powerpoint": [".ppt", ".pptx", ".pps", ".ppsx"],
    "autocad": [".dwg", ".dxf",".bak"],
    "sketchup": [".skp"],
    "photoshop": [".psd"],
    "codes": [".py", ".c"],
    "D5": [".d5", ".fbx", ".obj", ".dae", ".stl", ".3ds"]
}


# Define paths for sorted and excluded directories
in_all = os.path.join(From, "__SORTED__")

# Create the output directory if it doesn't exist
os.makedirs(in_all, exist_ok=True)

# Walk through the source directory
for dirpath, dirnames, filenames in os.walk(From):
    # Skip directories in the not_sort list or their subdirectories
    if "SORT" in dirpath.upper():
        continue
    for file in filenames:
        filepath = os.path.join(dirpath, file)  # Full path of the current file

        # Check the file's extension against the defined categories
        for category, ext_list in extensions.items():
            if file.lower().endswith(tuple(ext_list)):  # Use tuple for endswith
                # Create category folder if it doesn't exist
                category_folder = os.path.join(in_all, category)
                os.makedirs(category_folder, exist_ok=True)

                # Move the file to the corresponding category folder
                try:
                    shutil.move(filepath, category_folder)
                    print(f"Moved {file} to {category} Folder")
                except Exception as e:
                    print(f"Error moving {file}: {e}")
                break