#!/usr/bin/env python3
"""
Add Caesar Cipher challenge to CTFd
Run this inside the CTFd container or after setting up CTFd
"""

import os
import sys

# Add CTFd to path
sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Challenges, Flags, db
from CTFd import create_app

def add_caesar_challenge():
    """Add Caesar cipher challenge to CTFd database"""
    
    app = create_app()
    
    with app.app_context():
        # Check if challenge already exists
        existing = Challenges.query.filter_by(name="Caesar Cipher").first()
        if existing:
            print("Challenge already exists!")
            return
        
        # Create challenge
        challenge = Challenges(
            name="Caesar Cipher",
            description="""You have intercepted an encrypted message:
            
**Encrypted:** `Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj.`

Your task is to find the correct Caesar cipher shift value (0-25) to decrypt it.

Once decrypted, you will find instructions or a message containing the flag.

**Hint:** Try different shift values. Start with small numbers like 1, 2, 3...

**How to submit:** Run the caesar-challenge container, try different shifts until you decrypt the message and get the flag.

```
docker run -it caesar-cipher-challenge:latest
```
""",
            category="Cryptography",
            value=100,
            state="visible",
            type="standard"
        )
        
        db.session.add(challenge)
        db.session.commit()
        
        # Create flag
        flag = Flags(
            challenge_id=challenge.id,
            content="CTF{c43s4r_c1ph3r_m4st3r}",
            data="case_sensitive"
        )
        
        db.session.add(flag)
        db.session.commit()
        
        print(f"Challenge added successfully!")
        print(f"Challenge ID: {challenge.id}")
        print(f"Flag: {flag.content}")

if __name__ == "__main__":
    add_caesar_challenge()
