from fastapi import FastAPI
from core.tflog import TFLoggerManager as TFLog
from core.tfdb import TFDB
from api.router_manager import RouterManager

from datetime import datetime

import openai
from dotenv import load_dotenv
import os

#from core.tfconfig_manager import TFConfigManager as TFConfig

def configure_middleware(app: FastAPI):
    from fastapi.middleware.cors import CORSMiddleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def create_app() -> FastAPI:

    # 환경변수 로드
    load_dotenv()
    openai.api_key = os.getenv("OPENAI_API_KEY")

    logger = TFLog().get_logger() 
    routerMgr = RouterManager().get_instance()
    
    app = FastAPI()
    configure_middleware(app)
    routerMgr.include_routers(app)

    @app.on_event("startup")
    async def startup_event():
        logger.info("Start main")
        db = TFDB.get_instance()
        connected = await db.is_connected()
        if not connected:
            logger.critical("Error MongoDB Connect Fail!!!.")
        else:
            logger.info("Success MongoDB Connect")
            await db.create_collections()
            
        logger.info("Start complete")

    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("End main")

    @app.get("/")
    async def root():
        return {"message": "Connected FastAPI Server!!!"}

    @app.get("/time")
    async def root():
        now = datetime.now()
        return {"time": now.strftime("%Y-%m-%d %H:%M:%S")}


    @app.post("/chat")
    async def chat_with_gpt(request: ChatRequest):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",  # 또는 gpt-4 등
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": request.message}
                ]
            )
            return {"response": response.choices[0].message["content"]}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        
        return app

app = create_app()