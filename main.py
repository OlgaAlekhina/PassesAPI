from fastapi import FastAPI, status
import schemas


app = FastAPI()

@app.get("/")
def root():
    return "my pass api"


@app.post("/pass")
def submitData(passes: schemas.AddPass):
    passes.add_pass()
    return "cool!"