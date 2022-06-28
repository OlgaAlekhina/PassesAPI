from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from collections import defaultdict
from schemas import Response, AddPass, PassDetails, get_pass


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    response_message = defaultdict(list)
    for pydantic_error in exc.errors():
        loc, msg = pydantic_error["loc"], pydantic_error["msg"]
        filtered_loc = loc[1:] if loc[0] in ("body", "query", "path") else loc
        field_string = ".".join(filtered_loc)
        response_message[field_string].append(msg)
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content=jsonable_encoder(
            {"status": 400, "message": "Неправильно введены данные", "errors": response_message}
        ),
    )

@app.post("/addpass", response_model = Response)
def submitData(passes: AddPass):
    try:
        return Response(status=200, message="Отправлено успешно", id=passes.add_pass())

    except:
        return Response(status=500, message="Ошибка подключения к базе данных")


@app.get("/passes/{pass_id}", response_model=AddPass)
def get_pass_by_id(pass_id: int):
    return get_pass(pass_id)


# @app.patch("/update/{pass_id}")
# def update_pass_by_id(pass_id: int, passes: AddPass):
#     return 2#update_pass(pass_id)