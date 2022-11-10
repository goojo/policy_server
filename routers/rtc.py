from fastapi import APIRouter
import time

router = APIRouter()

@router.get("/time/")
async def fn_time():
    return {
        "time":time.time()
    }