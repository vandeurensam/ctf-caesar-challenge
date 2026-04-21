#!/usr/bin/env python3
"""
Check all challenges and their hints in CTFd
"""

import sys
sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Challenges, Hints, db
from CTFd import create_app

app = create_app()

with app.app_context():
    challenges = Challenges.query.all()
    
    print("=" * 70)
    print("CTFd CHALLENGES STATUS")
    print("=" * 70)
    print()
    
    for challenge in challenges:
        print(f"Challenge: {challenge.name}")
        print(f"  Category: {challenge.category}")
        print(f"  Points: {challenge.value}")
        print(f"  State: {challenge.state}")
        
        hints = Hints.query.filter_by(challenge_id=challenge.id).all()
        if hints:
            print(f"  Hints: {len(hints)} hints")
            for i, hint in enumerate(hints, 1):
                print(f"    {i}. {hint.content[:50]}... (Cost: {hint.cost})")
        else:
            print(f"  Hints: ❌ GEEN HINTS!")
        
        print()
