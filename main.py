from fastapi import FastAPI
from core.tflog import TFLoggerManager as TFLog
from core.tfdb import TFDB
#from core.tfconfig_manager import TFConfigManager as TFConfig

def include_routers(app: FastAPI):
    from api import routes_food_category, routes_fridge_item, routes_user_profile

    app.include_router(routes_food_category.router)
    app.include_router(routes_fridge_item.router)
    app.include_router(routes_user_profile.router)

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
    logger = TFLog().get_logger() 

    app = FastAPI()
    configure_middleware(app)
    include_routers(app)

    

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


    
    return app

app = create_app()