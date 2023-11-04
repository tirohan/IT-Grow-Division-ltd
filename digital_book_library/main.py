from fastapi import FastAPI
from digital_book_library.routers import books, authors, clients
from digital_book_library.database import database

app = FastAPI()

app.include_router(books.router)
app.include_router(authors.router)
app.include_router(clients.router)

@app.on_event("startup")
async def startup_db_client():
    database.connect()

@app.on_event("shutdown")
async def shutdown_db_client():
    database.disconnect()

if __name__ == "__main__":
    import uvicorn

    # You can start the application with uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)