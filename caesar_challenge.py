#!/usr/bin/env python3
"""
Caesar Cipher CTF Challenge
Decode the secret message to find the flag.
"""

def caesar_decrypt(ciphertext, shift):
    """Decrypt Caesar cipher with given shift."""
    result = []
    for char in ciphertext:
        if char.isalpha():
            if char.isupper():
                result.append(chr((ord(char) - ord('A') - shift) % 26 + ord('A')))
            else:
                result.append(chr((ord(char) - ord('a') - shift) % 26 + ord('a')))
        else:
            result.append(char)
    return ''.join(result)

def main():
    print("=" * 50)
    print("CAESAR CIPHER CHALLENGE")
    print("=" * 50)
    print()
    print("You have intercepted an encrypted message.")
    print("Find the correct shift value to decrypt it.")
    print()
    
    # Encrypted message (shifted by 3)
    encrypted = "Wkh txlfn eurzq ira mxpsv ryhu wkh odcb grj."
    
    print(f"Encrypted message: {encrypted}")
    print()
    
    while True:
        try:
            shift = int(input("Enter shift value (0-25): "))
            if shift < 0 or shift > 25:
                print("Shift must be between 0 and 25.")
                continue
            
            decrypted = caesar_decrypt(encrypted, shift)
            print(f"Decrypted: {decrypted}")
            
            # Check if correct (shift 3 is the answer)
            if shift == 3 and "The quick brown fox" in decrypted:
                print()
                print("=" * 50)
                print("CORRECT!")
                print("FLAG: CTF{c43s4r_c1ph3r_m4st3r}")
                print("=" * 50)
                break
            else:
                print("Not quite right. Try another shift.")
                print()
        
        except ValueError:
            print("Please enter a valid number.")
            print()

if __name__ == "__main__":
    main()
