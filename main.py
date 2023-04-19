import asyncio

from fastapi import Depends
from fastapi.responses import JSONResponse
from app import App
from jwt_auth import JWTAuth
from services import StatisticServices

app = App()
jwt_auth = JWTAuth()


@app.on_event('startup')
async def startup():
    loop = asyncio.get_running_loop()
    task = loop.create_task(app.pika_client.consume(loop))
    await task


@app.get("/get-statistic/{page_id}", status_code=200)
async def get_statistic(page_id: str, payload=Depends(jwt_auth.auth_wrapper)):
    user_id, page_id = payload.get('user_id'), int(page_id)
    data = await StatisticServices.get_item(user_id=user_id, page_id=page_id)
    return JSONResponse(content=data)
