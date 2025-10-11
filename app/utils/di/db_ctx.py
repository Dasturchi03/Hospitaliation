from contextvars import ContextVar
from typing import Optional, Callable, Union, cast

from starlette import requests
from fastapi import Depends, FastAPI
from fastapi.routing import APIRoute, APIRouter
from fastapi.dependencies.utils import get_parameterless_sub_dependant
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import async_session_manager


_current_session: ContextVar[Optional[AsyncSession]] = ContextVar("_current_session", default=None)


async def _db_ctx_dep(_: requests.Request):
    async with async_session_manager() as session:
        token = _current_session.set(session)
        try:
            yield session
        finally:
            _current_session.reset(token)


def get_db_from_ctx() -> AsyncSession:
    "Public getter"
    session = _current_session.get()
    if session is None:
        raise RuntimeError("DB session is not in context. Did you call add_db_ctx(app/router)?")
    return session


class _ContextVarProxy:
    __slots__ = ("_var", "_name")

    def __init__(self, var: ContextVar, name: str):
        object.__setattr__(self, "_var", var)
        object.__setattr__(self, "_name", name)

    def _get(self) -> AsyncSession:
        obj = self._var.get()
        if obj is None:
            raise RuntimeError(f"{self._name} is not in context. Did you call add_db_ctx?")
        return obj

    def __getattr__(self, item):
        return getattr(self._get(), item)

    def __setattr__(self, k, v):
        setattr(self._get(), k, v)

    def __repr__(self):
        try: target = self._get()
        except Exception: target = None
        return f"<ContextVarProxy {self._name} -> {target!r}>"

    def __bool__(self):
        try: return bool(self._get())
        except RuntimeError: return False


DB: AsyncSession = cast(AsyncSession, _ContextVarProxy(_current_session, "db session"))


def _marker():
    "For idempotention"
    pass


def _patch_route(route: APIRoute) -> None:
    if any(getattr(d, "call", None) is _marker for d in route.dependant.dependencies):
        return
    deps = [Depends(_marker), Depends(_db_ctx_dep)]

    route.dependencies = deps + route.dependencies
    route.dependant.dependencies = [
        get_parameterless_sub_dependant(depends=d, path=route.path_format) for d in deps
    ] + route.dependant.dependencies


def _ensure_router(obj: Union[FastAPI, APIRouter]) -> APIRouter:
    return obj.router if isinstance(obj, FastAPI) else obj


def add_db_ctx(target: Union[FastAPI, APIRouter]) -> None:
    router = _ensure_router(target)

    if getattr(router, "_db_ctx_patched", False):
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
    router.add_api_route = add_api_route_wrapper  # type: ignore

    orig_include_router = router.include_router
    def include_router_wrapper(r: APIRouter, *args, **kwargs):
        res = orig_include_router(r, *args, **kwargs)
        for rr in r.routes:
            if isinstance(rr, APIRoute):
                _patch_route(rr)
        if not getattr(r, "_db_ctx_patched", False):
            add_db_ctx(r)
        return res
    router.include_router = include_router_wrapper  # type: ignore

    setattr(router, '_db_ctx_patched', True)
