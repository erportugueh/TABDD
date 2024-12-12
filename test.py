import os
import re

# Specify the directory
directory = r"C:\Users\elmer\Downloads\Images\Images"

# Iterate through files in the directory
for filename in os.listdir(directory):
    # Match one or more digits at the beginning of the filename
    match = re.match(r'^(\d+)', filename)
    if match:
        new_name = match.group(1) + os.path.splitext(filename)[1]  # Keep the file extension
        old_path = os.path.join(directory, filename)
        new_path = os.path.join(r"C:\Users\elmer\Downloads\Images\new", new_name)

        # Rename the file
        os.rename(old_path, new_path)
        print(f"Renamed: {filename} -> {new_name}")

