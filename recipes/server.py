import uvicorn


def run():
    uvicorn.run("recipes.webapp:app", reload=True)
