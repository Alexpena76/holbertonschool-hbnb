"""
Bcrypt Password Hash Generator
Generates bcrypt hashes for passwords
"""

import bcrypt

def generate_hash(password):
    """
    Generate a bcrypt hash for the given password
    
    Args:
        password (str): Plain text password
        
    Returns:
        str: Bcrypt hash
    """
    # Generate salt and hash
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    
    return hashed.decode('utf-8')

def verify_hash(password, hashed):
    """
    Verify a password against its hash
    
    Args:
        password (str): Plain text password
        hashed (str): Bcrypt hash
        
    Returns:
        bool: True if password matches hash
    """
    return bcrypt.checkpw(password.encode('utf-8'), hashed.encode('utf-8'))

if __name__ == '__main__':
    # Generate hash for admin password
    admin_password = 'admin1234'
    admin_hash = generate_hash(admin_password)
    
    print("=" * 60)
    print("Password Hash Generator")
    print("=" * 60)
    print(f"\nPassword: {admin_password}")
    print(f"Hash: {admin_hash}")
    print(f"\nVerification: {verify_hash(admin_password, admin_hash)}")
    print("\n" + "=" * 60)
    
    # Generate additional hashes if needed
    test_password = 'test123'
    test_hash = generate_hash(test_password)
    print(f"\nTest Password: {test_password}")
    print(f"Test Hash: {test_hash}")
    print(f"\nVerification: {verify_hash(test_password, test_hash)}")
    print("\n" + "=" * 60)