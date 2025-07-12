from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
qr = FastAPI()

qr.mount("/",StaticFiles(directory="qrcode",html=True))