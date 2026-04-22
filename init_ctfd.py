#!/usr/bin/env python3
"""
Initialize CTFd with all challenges and hints
Runs automatically after CTFd starts
"""

import sys
import os
import time

sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Challenges, Hints, Flags, db
from CTFd import create_app

# Load environment variables from any available source
# Try .env file first, then fall back to env vars
def load_flags():
    """Load flags from environment or defaults"""
    
    flags = {
        'CAESAR_FLAG': os.getenv('CAESAR_FLAG', 'CTF{c43s4r_c1ph3r_m4st3r}'),
        'IMAGE_METADATA_FLAG': os.getenv('IMAGE_METADATA_FLAG', 'CTF{3x1f_m3t4d4t4_5ecr3t}'),
        'HTTP_HEADERS_FLAG': os.getenv('HTTP_HEADERS_FLAG', 'CTF{http_h34d3r_s3cr3t}'),
    }
    
    return flags

def wait_for_db(max_retries=30):
    """Wait for database to be ready"""
    for attempt in range(max_retries):
        try:
            app = create_app()
            with app.app_context():
                db.engine.execute("SELECT 1")
            print("✓ Database is ready!")
            return app
        except Exception as e:
            if attempt < max_retries - 1:
                print(f"Waiting for database... ({attempt + 1}/{max_retries})")
                time.sleep(1)
            else:
                print(f"❌ Database not ready after {max_retries} retries")
                raise

def add_challenges_and_hints():
    """Add all challenges, flags, and hints to CTFd"""
    
    app = wait_for_db()
    flags = load_flags()
    
    challenges_data = [
        {
            "name": "Caesar Cipher",
            "description": """You have intercepted an encrypted message:

**Encrypted:** `Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.`

Your task is to find the correct Caesar cipher shift value (0-25) to decrypt it.

Once decrypted, you will find the flag.

**How to solve:**
```bash
docker run -it docker-caesar-challenge
```

Try different shift values until the message becomes readable.""",
            "category": "Cryptography",
            "value": 100,
            "flag": flags['CAESAR_FLAG'],
            "hints": [
                {"content": "A Caesar cipher shifts each letter by a fixed number of positions in the alphabet.", "cost": 10},
                {"content": "Try shift values starting from 1. The correct one will make the message readable.", "cost": 20},
                {"content": "The first word of the decrypted message starts with 'T'.", "cost": 30},
                {"content": "The correct shift value is 3.", "cost": 50}
            ]
        },
        {
            "name": "Image Metadata",
            "description": """You have found a suspicious image file. The image looks innocent, but there's a secret hidden in its EXIF metadata.

**Challenge:** Extract the EXIF data and find the flag hidden in the image metadata.

**How to solve:**
```bash
docker run -it docker-image-challenge
```

Use the tools to inspect the image's metadata. EXIF data is stored inside image files and can contain hidden information.

**Hints:**
- EXIF data is metadata stored in image files
- Use exiftool to extract EXIF data
- Look at all metadata fields carefully
- The flag is hidden in one of the metadata fields""",
            "category": "Forensics",
            "value": 150,
            "flag": flags['IMAGE_METADATA_FLAG'],
            "hints": [
                {"content": "EXIF data is metadata embedded in image files like photos.", "cost": 10},
                {"content": "The exiftool command can extract all EXIF data from an image.", "cost": 20},
                {"content": "Look for fields like 'Make', 'Model', 'Software' - one of them contains the flag.", "cost": 30},
                {"content": "Check the 'Software' field - that's where the flag is hidden.", "cost": 50}
            ]
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
            "flag": flags['HTTP_HEADERS_FLAG'],
            "hints": [
                {"content": "HTTP headers are key-value pairs sent with HTTP responses.", "cost": 10},
                {"content": "Use browser DevTools (F12) → Network tab to inspect response headers.", "cost": 20},
                {"content": "Look for headers starting with 'X-' - they're custom headers that might contain hints.", "cost": 30},
                {"content": "The flag is hidden in the X-Flag-* headers and the X-Secret header. Combine them!", "cost": 50}
            ]
        }
    ]
    
    with app.app_context():
        print("=" * 70)
        print("Initializing CTFd with Challenges and Hints")
        print("=" * 70)
        print()
        
        for challenge_data in challenges_data:
            # Check if challenge already exists
            existing = Challenges.query.filter_by(name=challenge_data["name"]).first()
            if existing:
                print(f"ℹ️  Challenge '{challenge_data['name']}' already exists")
                # Ensure flag type is correct
                flag = Flags.query.filter_by(challenge_id=existing.id).first()
                if flag and (flag.type is None or flag.type != 'static'):
                    flag.type = "static"
                    db.session.commit()
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
                type="static"
            )
            
            db.session.add(flag)
            db.session.commit()
            
            # Create hints
            for hint_data in challenge_data["hints"]:
                hint = Hints(
                    challenge_id=challenge.id,
                    content=hint_data["content"],
                    cost=hint_data["cost"]
                )
                db.session.add(hint)
            
            db.session.commit()
            
            print(f"✓ Created: {challenge_data['name']} ({challenge_data['value']} pts)")
            print(f"  Flag: {challenge_data['flag']}")
            print(f"  Hints: {len(challenge_data['hints'])}")
            print()
        
        # Verify all challenges are visible and flags have correct type
        print("Verifying scoring setup...")
        all_challenges = Challenges.query.all()
        for challenge in all_challenges:
            if challenge.state != "visible":
                challenge.state = "visible"
                db.session.commit()
            
            flag = Flags.query.filter_by(challenge_id=challenge.id).first()
            if flag and (flag.type is None or flag.type != 'static'):
                flag.type = "static"
                db.session.commit()
        
        print()
        print("=" * 70)
        print("✓ CTFd initialization complete!")
        print("=" * 70)
        print()
        print("📍 Access points:")
        print("   - CTFd Dashboard: http://localhost:8000")
        print("   - HTTP Challenge: http://localhost:5000")
        print()
        print("💡 To earn points:")
        print("   1. Log in to CTFd")
        print("   2. Click on a challenge")
        print("   3. Submit the flag")
        print("   4. ✓ Points are added to your score!")
        print("   5. View your rank on the scoreboard")
        print()

if __name__ == "__main__":
    try:
        add_challenges_and_hints()
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
