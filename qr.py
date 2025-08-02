from fastapi import FastAPI,Path,Query,Form,Request
from starlette.middleware.sessions import SessionMiddleware
from typing import Annotated
from fastapi.responses import JSONResponse,PlainTextResponse,HTMLResponse,FileResponse,RedirectResponse 
from fastapi.staticfiles import StaticFiles
from MySql.mysql import SQL
from Image import IMG
import pyotp
import os
from dotenv import load_dotenv
from urllib.parse import urlparse
KEY = "KEY"
qr = FastAPI()

load_dotenv()
url = urlparse(os.getenv("MySqlPublicUrl"))
sql = SQL(USER = url.username,
          PASSWORD = url.password,
          HOST = url.hostname,
          PORT = url.port,
          DATABASE = url.path.lstrip("/"))

def TotpAuthenticatorObject(secret,CODE=False):
    obj = pyotp.TOTP(secret)
    if CODE:
        return obj.now()
    return obj
    
qr.add_middleware(SessionMiddleware,secret_key=KEY)
@qr.post("/login")
async def Login(request:Request):
    response = await request.json()
    email = response["email"]
    account = response["account"]
    password = response["password"]
    check = sql.execute(instruction = """SELECT *FROM login
                                         WHERE email=%s AND account=%s AND password=%s""",
                        SET = (email,account,password),
                        SELECT = True)
    if check:
        
        request.session["SECRET"] = pyotp.random_base32()
        
        Totp_object = TotpAuthenticatorObject(secret = request.session["SECRET"])
        
        uri = Totp_object.provisioning_uri(
            name=email,
            issuer_name="Google"
        )
        img_data_src = IMG.src(URI = uri)
        
        return JSONResponse({"status":True,
                             "qrcode":img_data_src,
                             "information":"qrcode已儲存，請掃描後輸入驗證碼",})
    else:
        return JSONResponse({"status":False})
    
@qr.post("/login/totp")
async def LoginTotp(request:Request):
    response = await request.json()
    totp_input = response["totp"]
    Totp_code = TotpAuthenticatorObject(secret = request.session["SECRET"],CODE=True)
    if totp_input == Totp_code:
        return JSONResponse({"status":True})
    else:
        return JSONResponse({"status":False})
qr.mount("/",StaticFiles(directory="web",html=True))


