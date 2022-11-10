from fastapi import FastAPI
from routers import policy, rtc

import uvicorn


app = FastAPI()

app.include_router(policy.router, tags=["policy"])
app.include_router(rtc.router, tags=["rtc"])

if __name__== "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
