import bcrypt

password = b"mysecretpassword"  # Password must be a byte string
hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())

print(hashed_password)