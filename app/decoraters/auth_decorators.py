from . import List, RoleEnum, HTTPException, wraps, inspect, asyncio, ic
from app.data_formats.typed_dicts.response_typdict import ResponseContentTypDict

def verify_role(allowed_roles: List[RoleEnum]):
    """Decorator to verify if the current user's role is in the allowed roles. 
    *Note, the first or second argument of the function,coroutine or object. 
    that should be as the 'current_user_role' attribute or parameter."""
    if not allowed_roles:
        raise ValueError("allowed_roles list cannot be empty.")

    def _extract_role(args, kwargs):
        # Case 1: method calls (self, ...)
        if args:
            # object with attribute
            if hasattr(args[0], "current_user_role"):
                return args[0].current_user_role

            # second argument
            if len(args) > 1 and hasattr(args[1], "current_user_role"):
                return args[1].current_user_role

            # positional param as role
            if isinstance(args[0], RoleEnum):
                return args[0]
            if len(args) > 1 and isinstance(args[1], RoleEnum):
                return args[1]

        # Case 2: keyword argument
        return kwargs.get("current_user_role")
    
    def decorator(func):
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            cur_user_role = _extract_role(args, kwargs)

            if cur_user_role not in allowed_roles:
                raise HTTPException(
                    status_code=403, 
                    detail=ResponseContentTypDict(
                        status=403,
                        msg="Error : Unauthorized Forbidden",
                        description="Access forbidden: insufficient permissions.",
                        succsess=False
                    )
                )

            return await func(*args, **kwargs)
        
        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            cur_user_role = _extract_role(args, kwargs)

            if cur_user_role not in allowed_roles:
                raise HTTPException(
                    status_code=403, 
                    detail=ResponseContentTypDict(
                        status=403,
                        msg="Error : Unauthorized Forbidden",
                        description="Access forbidden: insufficient permissions.",
                        succsess=False
                    )
                )

            return func(*args, **kwargs)

        return async_wrapper if inspect.iscoroutinefunction(func) else sync_wrapper

    return decorator


            
