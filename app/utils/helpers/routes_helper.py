"""Decorators for service functions to wrap them with try/except and DB session handling."""

import types
import logging
import inspect
from functools import wraps
from sqlalchemy.orm import Query, Session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql.selectable import Select
from fastapi_pagination.ext.sqlalchemy import paginate, apaginate
from app.core.db import session_manager, async_session_manager


logger = logging.getLogger(__name__)


def service(func):
    """Decorator for synchronous service handlers to manage DB session and pagination."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        with session_manager() as db:
            kwargs['db'] = db
            resp = func(*args, **kwargs)
            opts = getattr(resp, "__pagination_opts__", {})
            if isinstance(resp, Query):
                return paginate(resp, **opts)
            elif isinstance(resp, Select):
                return paginate(db, resp, **opts)
            return resp
    return wrapper


def async_service(func):
    """Decorator for asynchronous service handlers to manage DB session and pagination."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        async with async_session_manager() as db:
            kwargs['db'] = db
            resp = await func(*args, **kwargs)
            opts = getattr(resp, "__pagination_opts__", {})
            if isinstance(resp, Query):
                return await apaginate(resp, **opts)
            elif isinstance(resp, Select):
                return await apaginate(db, resp, **opts)
            return resp
    return wrapper


def wrap_func(func):
    "Wrapper function for wrapping service functions on initializate"
    if inspect.iscoroutinefunction(func):
        async def async_wrapped(*args, **kwargs):
            if 'db' in inspect.signature(func).parameters:
                db = kwargs.get('db', None)
                if isinstance(db, AsyncSession):
                    resp = await func(*args, **kwargs)
                    opts = getattr(resp, "__pagination_opts__", {})
                    if isinstance(resp, Query):
                        return await apaginate(resp, **opts)
                    elif isinstance(resp, Select):
                        return await apaginate(db, resp, **opts)
                else:
                    async with async_session_manager() as db:
                        kwargs.setdefault('db', db)
                        resp = await func(*args, **kwargs)
                        opts = getattr(resp, "__pagination_opts__", {})
                        if isinstance(resp, Query):
                            return await apaginate(resp, **opts)
                        elif isinstance(resp, Select):
                            return await apaginate(db, resp, **opts)
                return resp
            else:
                return await func(*args, **kwargs)
        return async_wrapped
    else:
        def sync_wrapped(*args, **kwargs):
            if 'db' in inspect.signature(func).parameters:
                if isinstance(kwargs.get('db', None), Session):
                    resp = func(*args, **kwargs)
                    opts = getattr(resp, "__pagination_opts__", {})
                    if isinstance(resp, Query):
                        return paginate(resp, **opts)
                    elif isinstance(resp, Select):
                        return paginate(db, resp, **opts)
                else:
                    with session_manager() as db:
                        kwargs.setdefault('db', db)
                        resp = func(*args, **kwargs)
                        opts = getattr(resp, "__pagination_opts__", {})
                        if isinstance(resp, Query):
                            return paginate(resp, **opts)
                        elif isinstance(resp, Select):
                            return paginate(db, resp, **opts)
                return resp
            else:
                return func(*args, **kwargs)
        return sync_wrapped


def wrap_modules(MODULES: list):
    for mod in MODULES:
        for attr_name in dir(mod):
            if not attr_name.startswith('_'):
                attr = getattr(mod, attr_name)

                if (
                    isinstance(attr, types.FunctionType)
                    and attr.__module__ == mod.__name__
                ):
                    setattr(mod, attr_name, wrap_func(attr))
