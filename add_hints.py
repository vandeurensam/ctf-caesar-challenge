#!/usr/bin/env python3
"""
Add hints to all CTF challenges in CTFd
"""

import sys
sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Challenges, Hints, db
from CTFd import create_app

app = create_app()

hints_data = {
    "Caesar Cipher": [
        {
            "content": "A Caesar cipher shifts each letter by a fixed number of positions in the alphabet.",
            "cost": 10
        },
        {
            "content": "Try shift values starting from 1. The correct one will make the message readable.",
            "cost": 20
        },
        {
            "content": "The first word of the decrypted message starts with 'T'.",
            "cost": 30
        },
        {
            "content": "The correct shift value is 3.",
            "cost": 50
        }
    ],
    "Image Metadata": [
        {
            "content": "EXIF data is metadata embedded in image files like photos.",
            "cost": 10
        },
        {
            "content": "The exiftool command can extract all EXIF data from an image.",
            "cost": 20
        },
        {
            "content": "Look for fields like 'Make', 'Model', 'Software' - one of them contains the flag.",
            "cost": 30
        },
        {
            "content": "Check the 'Software' field - that's where the flag is hidden.",
            "cost": 50
        }
    ],
    "HTTP Headers & Cookies": [
        {
            "content": "HTTP headers are key-value pairs sent with HTTP responses.",
            "cost": 10
        },
        {
            "content": "Use browser DevTools (F12) → Network tab to inspect response headers.",
            "cost": 20
        },
        {
            "content": "Look for headers starting with 'X-' - they're custom headers that might contain hints.",
            "cost": 30
        },
        {
            "content": "The flag is hidden in the X-Flag-* headers and the X-Secret header. Combine them!",
            "cost": 50
        }
    ]
}

with app.app_context():
    print("=" * 70)
    print("Adding Hints to CTF Challenges")
    print("=" * 70)
    print()
    
    for challenge_name, hints_list in hints_data.items():
        challenge = Challenges.query.filter_by(name=challenge_name).first()
        
        if not challenge:
            print(f"❌ Challenge '{challenge_name}' not found!")
            continue
        
        # Remove existing hints
        Hints.query.filter_by(challenge_id=challenge.id).delete()
        db.session.commit()
        
        # Add new hints
        for hint_data in hints_list:
            hint = Hints(
                challenge_id=challenge.id,
                content=hint_data["content"],
                cost=hint_data["cost"]
            )
            db.session.add(hint)
        
        db.session.commit()
        
        print(f"✓ Added {len(hints_list)} hints to '{challenge_name}'")
        for i, hint in enumerate(hints_list, 1):
            print(f"  {i}. Cost: {hint['cost']} pts - {hint['content'][:50]}...")
        print()
    
    print("=" * 70)
    print("All hints added successfully!")
    print("=" * 70)
