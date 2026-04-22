#!/usr/bin/env python3
"""
Fix flag types in CTFd - change 'data' to 'static'
"""

import sys
sys.path.insert(0, '/opt/CTFd')

from CTFd.models import Flags, db
from CTFd import create_app

app = create_app()

with app.app_context():
    # Find all flags with wrong type
    flags = Flags.query.all()
    
    print("Fixing flag types...")
    print()
    
    for flag in flags:
        if flag.type != 'static':
            print(f"Fixing flag: {flag.content}")
            print(f"  Old type: {flag.type}")
            flag.type = 'static'
            print(f"  New type: {flag.type}")
            db.session.commit()
    
    print()
    print("All flags fixed!")
