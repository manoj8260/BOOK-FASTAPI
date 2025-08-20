from  typing import Any , Callable
from  fastapi.requests import Request
from  fastapi.responses import JSONResponse
from fastapi import status
from fastapi import FastAPI


class BooklyExceptions(Exception):
    '''This is the base class for all the Bookly errors'''
    pass
class InvalidToken(BooklyExceptions):
    '''User has provided the invalid or expire token'''
    pass
class RevokedToken(BooklyExceptions):
    '''User has provided the token that has been revoked '''
    pass
class AccessTokenRequired(BooklyExceptions):
    '''User has provided the refresh token when the access toke is needed'''
    pass
class RefreshTokenRequired(BooklyExceptions):
    '''User has provided the access token when the refresh toke is needed'''
    pass
class UserAleradyExists(BooklyExceptions):
    '''The user has provide the email is alerady exists '''
    pass
class UserNotFound(BooklyExceptions):
    '''User is not avilavale (User is not Exists)'''
    pass
class PermissionError(BooklyExceptions):
    '''You are not Authorize to do this action'''
    pass
class BookNotFound(BooklyExceptions):
    '''Book not found'''
    pass
# internal server error
async def internal_server_error(request,exc):
    return JSONResponse(
        content={
            "message" : "OOPS ! somethings went wrong ",
            "error_code"  : "server error" 
        },
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
    ) 
def create_exception_handler(status_code: int , initial_detail :Any) -> Callable[[Request,Exception],JSONResponse] :
    async  def exception_handler(request : Request,exc : BooklyExceptions) -> JSONResponse :
        return JSONResponse(
            content=initial_detail,
            status_code=status_code
        )
    return  exception_handler    

# -------------------------------
# ✅ Centralized Exception Mapping
# -------------------------------
exception_handlers = {
    BookNotFound: {
        "status": status.HTTP_404_NOT_FOUND,
        "detail": {
            "message": "Book not found",
            "resolution": "Please provide a valid book id"
        }
    },
    InvalidToken: {
        "status": status.HTTP_403_FORBIDDEN,
        "detail": {
            "message": "Token is invalid or expired",
            "resolution": "Please provide a valid token"
        }
    },
    RevokedToken: {
        "status": status.HTTP_403_FORBIDDEN,
        "detail": {
            "message": "Token has been revoked",
            "resolution": "Please login again to continue"
        }
    },
    AccessTokenRequired: {
        "status": status.HTTP_401_UNAUTHORIZED,
        "detail": {
            "message": "Access token required",
            "resolution": "Please include a valid access token in headers"
        }
    },
    RefreshTokenRequired: {
        "status": status.HTTP_401_UNAUTHORIZED,
        "detail": {
            "message": "Refresh token required",
            "resolution": "Please include a valid refresh token"
        }
    },
    UserAleradyExists: {
        "status": status.HTTP_400_BAD_REQUEST,
        "detail": {
            "message": "User already exists",
            "resolution": "Please use a different email or username"
        }
    },
    UserNotFound: {
        "status": status.HTTP_404_NOT_FOUND,
        "detail": {
            "message": "User not found",
            "resolution": "Please check the user id or email"
        }
    },
    PermissionError: {
        "status": status.HTTP_403_FORBIDDEN,
        "detail": {
            "message": "Permission denied",
            "resolution": "You don’t have permission to perform this action"
        }
    },
}


# -------------------------------
# ✅ Register all handlers in a loop
# -------------------------------

def register_exception_handlers(app :FastAPI):
    for exc_class, cfg in exception_handlers.items():
     app.add_exception_handler(
        exc_class,
        create_exception_handler(
            status_code=cfg["status"],
            initial_detail=cfg["detail"]
        )
     )
     app.add_exception_handler(Exception,internal_server_error)