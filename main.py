from fastapi import FastAPI, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder
from collections import defaultdict
from schemas import Response, AddPass, get_pass, PassOptional, pass_details, ResponseUpdate, get_user_passes


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


@app.patch("/update/{pass_id}", response_model=ResponseUpdate)
def update_pass_by_id(pass_id: int, passes: PassOptional):
    try:
        stored_data = pass_details(pass_id)
        if stored_data:
            if stored_data.get("status") == "new":
                stored_model = PassOptional(**stored_data)
                update_data = passes.dict(exclude_unset=True)
                updated_pass = stored_model.copy(update=update_data)
                updated_pass.update_pass(pass_id)
                return ResponseUpdate(state=1, message="Успешное обновление")
            else:
                return ResponseUpdate(state=0, message="Нельзя редактировать эту запись")
        else:
            return ResponseUpdate(state=0, message="Перевал не найден")
    except:
        return ResponseUpdate(state=0, message="Ошибка подключения к базе данных")


@app.get("/passes/users/{user_email}")
def get_passes_by_email(user_email: str):
    return get_user_passes(user_email)

