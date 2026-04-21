#!/usr/bin/env python3
"""
Fix Caesar Cipher challenge - use correct flag type
"""

import os
import sys

sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Challenges, Flags, db
from CTFd import create_app

def fix_caesar_challenge():
    """Fix the flag type for the Caesar cipher challenge"""
    
    app = create_app()
    
    with app.app_context():
        # Find the challenge
        challenge = Challenges.query.filter_by(name="Caesar Cipher").first()
        
        if not challenge:
            print("Challenge not found!")
            return
        
        # Delete existing flags
        Flags.query.filter_by(challenge_id=challenge.id).delete()
        
        # Add new flag with correct type
        flag = Flags(
            challenge_id=challenge.id,
            content="CTF{c43s4r_c1ph3r_m4st3r}",
            data="static"
        )
        
        db.session.add(flag)
        db.session.commit()
        
        print("Challenge fixed!")
        print(f"Flag type: static")
        print(f"Flag content: CTF{c43s4r_c1ph3r_m4st3r}")

if __name__ == "__main__":
    fix_caesar_challenge()
