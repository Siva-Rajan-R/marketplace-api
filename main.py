from fastapi import FastAPI
from app.api.v1.routes.crud_routes import inventory_route,product_route,order_route,shop_route,employee_route,account_route
from starlette.middleware.cors import CORSMiddleware
from app.api.v1.routes.auth_routes import reg_log_route,accept_route
from app.database.configs.pg_config import init_pg_db
from contextlib import asynccontextmanager
from icecream import ic
from dotenv import load_dotenv
import os
load_dotenv()


@asynccontextmanager
async def app_lifespan(app:FastAPI):
    try:
        ic("🚀 Executing App Lifespan...")
        # await init_pg_db()
        yield

    except Exception as e:
        ic(f"Error : Staring App Lifespan {e}")
    
    finally:
        ic("👋 Finishing App Lifespan...")


# creating app based on environment
docs_url="/docs"
redoc_url="/redoc"
openapi_url="/openapi.json"
debug=True

if os.getenv("ENVIRONMENT")=="production":
    docs_url=None
    redoc_url=None
    openapi_url=None
    debug=False

app=FastAPI(
    lifespan=app_lifespan,
    title="Market-Place API",
    version="0.1.2",
    description="This is a Market-palce API, this data only be shown on developement !",
    docs_url=docs_url,
    redoc_url=redoc_url,
    openapi_url=openapi_url,
    debug=debug,
    
)


# register the routes

@app.get('/')
def home_root():
    return {
        'msg':'hi this is from marketplace api, if you are an user please go back to our site https://marketplace.com/'
    }

app.include_router(reg_log_route.v1_router,prefix='/api/v1')
app.include_router(accept_route.v1_router,prefix='/api/v1')
app.include_router(account_route.v1_router,prefix='/api/v1')
app.include_router(shop_route.v1_router,prefix='/api/v1')
app.include_router(employee_route.v1_router,prefix='/api/v1')
app.include_router(product_route.v1_router,prefix='/api/v1')
app.include_router(inventory_route.v1_router,prefix='/api/v1')
app.include_router(order_route.v1_router,prefix='/api/v1')





# regisetr the middlewared
app.add_middleware(
    CORSMiddleware,
    allow_credentials=True,
    allow_headers=["*"],
    allow_methods=["*"],
    allow_origins=["*"],
)


# register custom responses

