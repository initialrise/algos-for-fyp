from fastapi import APIRouter
from totp import get_totp_token
from pydantic import BaseModel

totp_router = APIRouter()

class TOTP(BaseModel):
    service_provider:str
    secret:str

mockkeys  = [["facebook","MZQWGZLCN5XWW==="],["google","M5XW6Z3MMU======"],["youtube","PFXXK5DVMJSQ===="]]

@totp_router.get("/getTOTP")
def getTOTP()-> list:
    # ideally need to return list of otp with their service provider , so fetch from db, loop and return
    #mockkeys  = [["facebook","MZQWGZLCN5XWW==="],["google","M5XW6Z3MMU======"],["youtube","PFXXK5DVMJSQ===="]]
    otplist = []
    for keys in mockkeys:
        otp = get_totp_token(keys[1])
        otplist.append([keys[0],otp])
    return otplist
    

@totp_router.post("/addTOTP")
def addTOTP(totp:TOTP):
    mockkeys.append([totp.service_provider,totp.secret])
    return {"message":"Added TOTP"}
#save secret to db along with its service provider
