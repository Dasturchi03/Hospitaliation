from typing import Any
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder


class AddedResponse(JSONResponse):
    def __init__(self, data: Any = None, message: str = "Successfully added"):
        response_content = {"message": message}
        if data is not None:
            response_content["data"] = data
        super().__init__(
            status_code=201,
            content=jsonable_encoder(response_content, exclude_none=True)
        )


class UpdatedResponse(JSONResponse):
    def __init__(self, data: Any = None, message: str = "Successfully updated"):
        response_content = {"message": message}
        if data is not None:
            response_content["data"] = data
        super().__init__(
            status_code=200,
            content=jsonable_encoder(response_content, exclude_none=True)
        )


class DeletedResponse(JSONResponse):
    def __init__(self, data: Any = None, message: str = "Successfully deleted"):
        response_content = {"message": message}
        if data is not None:
            response_content["data"] = data
        super().__init__(
            status_code=200,
            content=jsonable_encoder(response_content, exclude_none=True)
        )
