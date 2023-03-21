from passlib.hash import sha256_crypt
password = sha256_crypt.encrypt("TEST")
password2 = sha256_crypt.encrypt("TEST")
print(password)
print(password2)
verify = sha256_crypt.verify("TeST", password)
print(verify)