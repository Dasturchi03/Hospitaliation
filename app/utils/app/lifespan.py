import os
import tempfile
from fastapi import FastAPI
from contextlib import asynccontextmanager

if os.name == "nt":
    import msvcrt
    _IS_WINDOWS = True
else:
    import fcntl
    _IS_WINDOWS = False


LOCK_PATH = os.path.join(tempfile.gettempdir(), "app_scheduler.lock")


def try_acquire_lock():
    f = None
    try:
        f = open(LOCK_PATH, "a+")
        if _IS_WINDOWS:
            # 1 baytlik non-blocking lock
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            # Exclusive + non-blocking
            fcntl.flock(f.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB) # type: ignore
        return f
    except OSError:
        if f:
            try:
                f.close()
            except Exception:
                pass
        return None


def release_lock(lock_file):
    if not lock_file:
        return
    try:
        if _IS_WINDOWS:
            lock_file.seek(0)
            msvcrt.locking(lock_file.fileno(), msvcrt.LK_UNLCK, 1)
        else:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_UN) # type: ignore
    except OSError:
        pass
    finally:
        try:
            lock_file.close()
        except Exception:
            pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    import os
    # from app.utils.scheduler.aps import scheduler, INTERVAL_JOBS
    # from app.utils.clients import (httpx_client,
    #                             #    redis_client,
    #                                minio_client)

    is_leader_env = os.getenv('IS_LEADER')
    lock_fd = None

    if is_leader_env == '1':
        is_leader = True
    elif is_leader_env == '0':
        is_leader = False
    else:
        lock_fd = try_acquire_lock()
        is_leader = lock_fd is not None

    # app.state.httpx_client = httpx_client.get_client()
    # app.state.httpx_proxy_client = httpx_client.get_proxy_client()

    # app.state.redis_client = redis_client.get_client()

    # app.state.minio_client = minio_client.get_client()

    # if is_leader:
    #     scheduler.start()
    #     for job in INTERVAL_JOBS:
    #         scheduler.add_job(job, 'interval', days=1)

    try:
        yield
    finally:
        # if is_leader:
        #     scheduler.shutdown()

        if lock_fd:
            release_lock(lock_fd)

        # await httpx_client.aclose_clients()

        # await redis_client.aclose_client()
