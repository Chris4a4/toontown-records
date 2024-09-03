from fastapi import FastAPI

from api.routers.leaderboards import leaderboards_router

app = FastAPI(title='Toontown Records Public API',
              version='0.0.1'
              )
app.include_router(leaderboards_router)
