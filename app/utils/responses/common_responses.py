from typing import Any
from fastapi.responses import JSONResponse


class AddedResponse(JSONResponse):
    def __init__(self, data: Any = None, message: str = "Successfully added"):
        response_content = {"message": message}
        if data:
            response_content["data"] = data
        super().__init__(
            status_code=201,
            content=response_content
        )


class UpdatedResponse(JSONResponse):
    def __init__(self, data: Any = None, message: str = "Successfully updated"):
        response_content = {"message": message}
        if data:
            response_content["data"] = data
        super().__init__(
            status_code=200,
            content=response_content
        )


class DeletedResponse(JSONResponse):
    def __init__(self, data: Any = None, message: str = "Successfully deleted"):
        super().__init__(
            status_code=204,
            content=None
        )
