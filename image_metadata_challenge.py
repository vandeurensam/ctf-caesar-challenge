#!/usr/bin/env python3
"""
Image Metadata CTF Challenge
Find the flag hidden in the EXIF metadata of an image
"""

import os
from PIL import Image
from PIL.ExifTags import TAGS
import piexif

# Get flag from environment variable
FLAG = os.getenv('IMAGE_METADATA_FLAG', 'CTF{default_flag}')

def create_challenge_image():
    """Create a test image with hidden flag in EXIF metadata"""
    
    # Create a simple image
    img = Image.new('RGB', (200, 200), color='red')
    
    # Create EXIF data with hidden flag
    exif_dict = {
        "0th": {
            piexif.ImageIFD.Make: b"Canon",
            piexif.ImageIFD.Model: b"Canon EOS 5D",
            piexif.ImageIFD.Software: FLAG.encode('utf-8'),  # Flag hidden here!
            piexif.ImageIFD.ImageDescription: b"Vacation photo",
        }
    }
    
    exif_bytes = piexif.dump(exif_dict)
    img.save("challenge_image.jpg", "jpeg", exif=exif_bytes)
    print("Challenge image created: challenge_image.jpg")

def display_challenge():
    """Display the challenge to the user"""
    print("=" * 60)
    print("IMAGE METADATA CHALLENGE")
    print("=" * 60)
    print()
    print("You have found a suspicious image file: challenge_image.jpg")
    print()
    print("The image looks innocent, but there's a secret hidden in its")
    print("metadata. Use tools to inspect the image's EXIF data.")
    print()
    print("=" * 60)
    print("HINTS:")
    print("=" * 60)
    print("1. EXIF data is metadata stored inside image files")
    print("2. Use 'exiftool' to extract EXIF data:")
    print("   exiftool challenge_image.jpg")
    print()
    print("3. Or use Python with PIL/piexif to read it")
    print("4. Look carefully at all metadata fields")
    print()
    print("=" * 60)

def read_metadata_from_file():
    """Read and display metadata from the image"""
    print()
    print("=" * 60)
    print("EXTRACTING METADATA...")
    print("=" * 60)
    print()
    
    try:
        img = Image.open("challenge_image.jpg")
        exif_data = piexif.load("challenge_image.jpg")
        
        print("Image Properties:")
        print(f"  Format: {img.format}")
        print(f"  Size: {img.size}")
        print()
        
        print("EXIF Data Found:")
        print("-" * 60)
        
        for ifd_name in ("0th", "Exif", "GPS", "1st"):
            ifd = exif_data.get(ifd_name)
            if not ifd:
                continue
                
            for tag in ifd:
                tag_name = piexif.TAGS[ifd_name][tag]["name"]
                value = ifd[tag]
                
                # Try to decode if it's bytes
                if isinstance(value, bytes):
                    try:
                        value = value.decode('utf-8', errors='ignore')
                    except:
                        pass
                
                print(f"  {tag_name}: {value}")
        
        print()
        print("=" * 60)
        
    except Exception as e:
        print(f"Error reading metadata: {e}")

def main():
    # Create the challenge image
    if not os.path.exists("challenge_image.jpg"):
        create_challenge_image()
    
    # Display challenge
    display_challenge()
    
    # Ask user if they want help
    print("Type 'help' to extract and display metadata")
    print("Type 'exit' to quit")
    print()
    
    while True:
        user_input = input("> ").strip().lower()
        
        if user_input == 'exit':
            print("Goodbye!")
            break
        elif user_input == 'help':
            read_metadata_from_file()
            print()
            print("Found the flag? Submit it to CTFd!")
            print()
        else:
            print("Invalid command. Type 'help' or 'exit'")

if __name__ == "__main__":
    main()
