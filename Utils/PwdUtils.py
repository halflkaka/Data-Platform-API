from passlib.hash import pbkdf2_sha256


def set_password(raw_password):
    return  pbkdf2_sha256.encrypt(raw_password, rounds=200000, salt_size=16)


def verify_password(password, hash):
    return pbkdf2_sha256.verify(password, hash)

