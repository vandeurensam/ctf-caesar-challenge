#!/usr/bin/env python3
"""
Setup CTFd properly for scoring
"""

import sys
sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Challenges, Flags, db
from CTFd import create_app

app = create_app()

with app.app_context():
    print("=" * 70)
    print("Setting up CTFd for Scoring")
    print("=" * 70)
    print()
    
    # 1. Verify all challenges are visible and active
    print("1️⃣  Verifying challenges...")
    challenges = Challenges.query.all()
    for challenge in challenges:
        if challenge.state != "visible":
            challenge.state = "visible"
            db.session.commit()
        print(f"   ✓ {challenge.name} - visible, {challenge.value} pts")
    print()
    
    # 2. Verify flags
    print("2️⃣  Verifying flags...")
    flags = Flags.query.all()
    for flag in flags:
        challenge = Challenges.query.get(flag.challenge_id)
        if flag.type is None or flag.type != 'static':
            flag.type = "static"
            db.session.commit()
        print(f"   ✓ {challenge.name}: {flag.content[:30]}... (type: {flag.type})")
    print()
    
    print("=" * 70)
    print("✓ All challenges configured for scoring!")
    print("=" * 70)
    print()
    print("To earn points:")
    print("1. Visit http://localhost:8000")
    print("2. Log in with your admin account")
    print("3. Click on a challenge")
    print("4. Submit the flag")
    print("5. Points appear on scoreboard!")
    print()
