from passlib.context import CryptContext

context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class Hasher:
    @staticmethod
    def hash_password(plain_password: bytes):
        return context.hash(plain_password)

    @staticmethod
    def verify_password(plain_password: bytes, hashed_password: bytes):
        return context.verify(plain_password, hashed_password)
