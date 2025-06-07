from exception.errorfile import TokenExpiredException, TokenNoFoundException
from fastapi import FastAPI, staticfiles, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from api.routers import all_routers
from fastapi.requests import Request
import uvicorn

app = FastAPI(
    title="Упрощенный аналог Jira/Asana"
)

app.mount('/static', staticfiles.StaticFiles(directory='templates'), name='templates')


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Разрешить запросы с любых источников. Можете ограничить список доменов
    allow_credentials=True,
    allow_methods=["*"],  # Разрешить все методы (GET, POST, PUT, DELETE и т.д.)
    allow_headers=["*"],  # Разрешить все заголовки
)


@app.get("/")
async def redirect_to_auth():
    return RedirectResponse(url="/auth")


@app.exception_handler(TokenExpiredException)
async def token_expired_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")


# Обработчик для TokenNoFound
@app.exception_handler(TokenNoFoundException)
async def token_no_found_exception_handler(request: Request, exc: HTTPException):
    # Возвращаем редирект на страницу /auth
    return RedirectResponse(url="/auth")



for router in all_routers:
    app.include_router(router)


if __name__ == "__main__":
    uvicorn.run(app="main:app", reload=True)













