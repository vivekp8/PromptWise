from passlib.context import CryptContext
import sys

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

try:
    password = "testpassword"
    hashed = pwd_context.hash(password)
    print(f"Hashed: {hashed}")
    verified = pwd_context.verify(password, hashed)
    print(f"Verified: {verified}")
except Exception as e:
    print(f"Error during hashing/verification: {e}")
    sys.exit(1)
