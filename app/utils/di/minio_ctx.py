from typing import Optional, Union, Callable, Any, cast, TYPE_CHECKING
from contextvars import ContextVar

from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute, APIRouter
from fastapi.dependencies.utils import get_parameterless_sub_dependant
from starlette.requests import Request


if TYPE_CHECKING:
    from minio import Minio


_current_minio: ContextVar[Optional["Minio"]] = ContextVar("_current_minio", default=None)


async def _minio_ctx_dep(request: Request):
    client: "Minio" = request.app.state.minio_client
    token = _current_minio.set(client)
    try:
        yield client
    finally:
        _current_minio.reset(token)


def get_minio_from_ctx() -> "Minio":
    client = _current_minio.get()
    if client is None:
        raise RuntimeError(
            "MinIO client is not in context. Call add_minio_client(router/app) AFTER routes "
            "or use the patched variant below that hooks add_api_route."
        )
    return client


def _marker() -> None:
    pass


def _patch_route(route: APIRoute) -> None:
    if any(getattr(d, "call", None) is _marker for d in route.dependant.dependencies):
        return

    deps = [Depends(_marker), Depends(_minio_ctx_dep)]
    route.dependencies.extend(deps)
    route.dependant.dependencies.extend(
        get_parameterless_sub_dependant(depends=d, path=route.path_format) for d in deps
    )


def _ensure_router(obj: Union[FastAPI, APIRouter]) -> APIRouter:
    return obj.router if isinstance(obj, FastAPI) else obj


def add_minio_client(target: Union[FastAPI, APIRouter]) -> None:
    router = _ensure_router(target)

    if getattr(router, "_minio_ctx_patched", False):
        for r in router.routes:
            if isinstance(r, APIRoute):
                _patch_route(r)
        return

    for r in router.routes:
        if isinstance(r, APIRoute):
            _patch_route(r)

    orig_add_api_route: Callable = router.add_api_route

    def add_api_route_wrapper(*args, **kwargs):
        res = orig_add_api_route(*args, **kwargs)

        last = router.routes[-1]
        if isinstance(last, APIRoute):
            _patch_route(last)
        return res

    router.add_api_route = add_api_route_wrapper  # type: ignore[assignment]

    orig_include_router = router.include_router

    def include_router_wrapper(r: APIRouter, *args, **kwargs):
        res = orig_include_router(r, *args, **kwargs)

        for rr in r.routes:
            if isinstance(rr, APIRoute):
                _patch_route(rr)

        if not getattr(r, "_minio_ctx_patched", False):
            add_minio_client(r)
        return res

    router.include_router = include_router_wrapper  # type: ignore[assignment]

    setattr(router, '_minio_ctx_patched', True)


class _ContextVarProxy:
    __slots__ = ("_var", "_name")

    def __init__(self, var: ContextVar, name: str):
        object.__setattr__(self, "_var", var)
        object.__setattr__(self, "_name", name)

    def _get(self):
        obj = self._var.get()
        if obj is None:
            raise RuntimeError(f"{self._name} is not in context. Did you call add_minio_client(...)?")
        return obj

    def __getattr__(self, item: str) -> Any:
        return getattr(self._get(), item)

    def __setattr__(self, key: str, value: Any) -> None:
        setattr(self._get(), key, value)

    def __repr__(self) -> str:
        try:
            target = self._get()
        except Exception:
            target = None
        return f"<ContextVarProxy {self._name} -> {target!r}>"

    def __bool__(self) -> bool:
        try:
            return bool(self._get())
        except RuntimeError:
            return False


minio_client: "Minio" = cast("Minio", _ContextVarProxy(_current_minio, "minio"))
