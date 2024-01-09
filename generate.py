from fastapi import FastAPI
import random
import string
from totp_routes import totp_router


app = FastAPI()

app.include_router(totp_router)
@app.get("/generate")
def generate()->dict:
    passlen = 14
    characterSet = string.ascii_letters+string.digits+string.punctuation
    password = []
    for i in range(0,passlen):
        randchar = random.choice(characterSet)
        password.append(randchar)
    return {"password":"".join(password)}


