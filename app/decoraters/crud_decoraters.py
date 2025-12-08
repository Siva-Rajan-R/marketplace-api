import inspect,asyncio
from functools import wraps
from fastapi import HTTPException
from icecream import ic
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict

def catch_errors(func):
    if inspect.iscoroutinefunction(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                ic(f"Error at {func.__name__} -> {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=ResponseContentTypDict(
                        status=500,
                        msg="Error : Internal server error",
                        description="Try agin the request after sometimes , if it's persist. contact our team support@debuggers.com",
                        succsess=False
                    )
                )
        return wrapper

    else:
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except HTTPException:
                raise
            except Exception as e:
                ic(f"Error at {func.__name__} -> {e}")
                raise HTTPException(
                    status_code=500, 
                    detail=ResponseContentTypDict(
                        status=500,
                        msg="Error : Internal server error",
                        description="Try agin the request after sometimes , if it's persist. contact our team support@debuggers.com",
                        succsess=False
                    )
                )
            
        return wrapper



def start_db_transaction(func):
    """Decorator to start a database transaction. 
    *Note, the first argument of the function,coroutine or object. that should be as the 'session' attribute or parameter.
    """
    @wraps(func)
    async def async_wrapper(*args,**kwargs):
        session=None
        if args:
            if hasattr(args[0],"session"):
                session = args[0].session
            else:
                session = args[0]
        else:
            session = kwargs.get("session",None)

        if not session:
            raise ValueError("No session found to start the transaction.")
        
        if session.in_transaction() or session.in_nested_transaction():
            ic("Transaction already active → skipping begin()")
            return await func(*args, **kwargs)
        
        ic(f"Started transaction from async with session of: {session}")
        async with session.begin():
            return await func(*args,**kwargs)
        
    @wraps(func)
    def sync_wrapper(*args,**kwargs):
        session=None
        if args:
            if hasattr(args[0],"session"):
                session = args[0].session
            else:
                session = args[0]
        else:
            session = kwargs.get("session",None)

        if not session:
            raise ValueError("No session found to start the transaction.")
        
        if session.in_transaction() or session.in_nested_transaction():
            ic("Transaction already active → skipping begin()")
            return func(*args, **kwargs)
        
        ic(f"Started transaction from sync with session of: {session}")
        with session.begin():
            return func(*args,**kwargs)

    if inspect.iscoroutinefunction(func):
        return async_wrapper
    else:
        return sync_wrapper
