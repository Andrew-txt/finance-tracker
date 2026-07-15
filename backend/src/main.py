# Organize the code in this file later
import uvicorn
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse

from src.wallets.application.controllers import router as wallets_router
from src.operations.application.controllers import router as operations_router
from src.users.application.controllers import router as users_router

import src.operations.application.controllers as operations_module
import src.wallets.application.controllers as wallets_module
import src.users.application.controllers as users_module

from src.building_blocks.sqlalchemy_db_models import Base
from src.building_blocks.di import Container

app = FastAPI()

 
@app.get("/api/v1/health")
def healthcheck():
    return JSONResponse(status_code=status.HTTP_200_OK, content={"status": "healthy"})


app.include_router(wallets_router, prefix="/api/v1")
app.include_router(operations_router, prefix="/api/v1")
app.include_router(users_router, prefix="/api/v1")

container = Container()
container.wire(modules=[
    operations_module,
    wallets_module,
    users_module
])

engine = container.db_engine()
Base.metadata.create_all(bind=engine)

# if __name__ == "__main__":
#     uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)