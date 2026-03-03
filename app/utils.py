from passlib.context import CryptContext #pip uninstall bcrypt passlib -y ,pip install bcrypt==4.0.1,pip install passlib[bcrypt]
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #cryptContext = cryptocontext

def hash(password: str):
    return pwd_context.hash(password)

def verify(plain_password, hashed_password):
    return pwd_context.verify(plain_password,hashed_password)