#!/usr/bin/env python3
"""
Add all CTF challenges to CTFd
- Caesar Cipher
- Image Metadata (EXIF)
- HTTP Headers & Cookies

Flags are read from environment variables (.env file)
"""

import sys
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv()

sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Challenges, Flags, db
from CTFd import create_app

def add_challenges():
    """Add all challenges to CTFd"""
    
    # Get flags from environment
    challenges_data = [
        {
            "name": "Caesar Cipher",
            "description": """You have intercepted an encrypted message:

**Encrypted:** `Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.`

Your task is to find the correct Caesar cipher shift value (0-25) to decrypt it.

Once decrypted, you will find the flag.

**How to solve:**
```bash
docker run -it caesar-challenge
```

Try different shift values until the message becomes readable.""",
            "category": "Cryptography",
            "value": 100,
            "flag": os.getenv('CAESAR_FLAG', 'CTF{default_caesar}')
        },
        {
            "name": "Image Metadata",
            "description": """You have found a suspicious image file. The image looks innocent, but there's a secret hidden in its EXIF metadata.

**Challenge:** Extract the EXIF data and find the flag hidden in the image metadata.

**How to solve:**
```bash
docker run -it image-challenge
```

Use the tools to inspect the image's metadata. EXIF data is stored inside image files and can contain hidden information.

**Hints:**
- EXIF data is metadata stored in image files
- Use exiftool to extract EXIF data
- Look at all metadata fields carefully
- The flag is hidden in one of the metadata fields""",
            "category": "Forensics",
            "value": 150,
            "flag": os.getenv('IMAGE_METADATA_FLAG', 'CTF{default_image}')
        },
        {
            "name": "HTTP Headers & Cookies",
            "description": """A flag is hidden somewhere in HTTP response headers or cookies!

**Challenge:** Find the flag by inspecting HTTP responses. It could be in headers, cookies, or even the response body.

**How to access:**
Open http://localhost:5000 in your browser

**Tools available:**
1. Fetch Response Headers - Extract all response headers
2. Check Cookies - View all cookies
3. Inspect Full Response - See the full response data

**Browser DevTools Method:**
1. Press F12 or right-click → Inspect
2. Go to Network tab
3. Refresh the page
4. Check Response Headers for suspicious entries
5. Check Application/Storage for cookies

**Hints:**
- HTTP headers are metadata sent with responses
- Cookies are stored in Set-Cookie headers
- Some information might be hidden in headers you don't normally see
- Look for headers starting with "X-"
- The flag might be split across multiple headers""",
            "category": "Web",
            "value": 100,
            "flag": os.getenv('HTTP_HEADERS_FLAG', 'CTF{default_http}')
        }
    ]
    
    app = create_app()
    
    with app.app_context():
        for challenge_data in challenges_data:
            # Check if challenge already exists
            existing = Challenges.query.filter_by(name=challenge_data["name"]).first()
            if existing:
                print(f"Challenge '{challenge_data['name']}' already exists, skipping...")
                continue
            
            # Create challenge
            challenge = Challenges(
                name=challenge_data["name"],
                description=challenge_data["description"],
                category=challenge_data["category"],
                value=challenge_data["value"],
                state="visible",
                type="standard"
            )
            
            db.session.add(challenge)
            db.session.commit()
            
            # Create flag
            flag = Flags(
                challenge_id=challenge.id,
                content=challenge_data["flag"],
                data="static"
            )
            
            db.session.add(flag)
            db.session.commit()
            
            print(f"✓ Added challenge: {challenge_data['name']} ({challenge_data['value']} pts)")
            print(f"  Flag: {challenge_data['flag']}")
            print()

if __name__ == "__main__":
    print("=" * 60)
    print("Adding CTF Challenges to CTFd")
    print("=" * 60)
    print()
    add_challenges()
    print("=" * 60)
    print("All challenges added successfully!")
    print("=" * 60)
