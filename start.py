from uvicorn import run

if __name__ == "__main__":
    run("main:app", reload=True, debug=True, workers=4)

