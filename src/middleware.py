from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import JSONResponse
from fastapi import  status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
import time
import logging

logger = logging.getLogger('uvicorn.access')
logger.disabled =True


def register_middleware(app : FastAPI):
    
    @app.middleware('http')
    async def add_process_time_header(request:Request, call_next ):
        start_time = time.time()
        # print('after ', start_time)
        response = await call_next(request)
        processing_time = time.time() - start_time
        # print('process after :' , processing_time )
        # response.headers["X-Process-Time"] = str(processing_time)
        message = f" {request.method} - {request.client.host}:{request.client.port} - {request.url.path} - {response.status_code} -completed after : {processing_time}"
        print(message)
        return response
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins  =['*'],
        allow_methods = ['*'],
        allow_headers = ['*'] ,
        allow_credentials = True     
    )
    
    app.add_middleware(
        TrustedHostMiddleware ,
         allowed_hosts = ['*']
    )
    
    # @app.middleware('http')
    # async  def check_authentication(request:Request,call_next) :
    #     if not 'Authorization' in request.headers:
    #         return JSONResponse(
    #             content= {
    #                 'message' : 'Not authentication',
    #                 'resulation' : 'please provided the authentication crendential'
    #             },
    #             status_code=status.HTTP_403_FORBIDDEN
    #         )   
    #     response = await call_next(request)
    #     return  response
            
        
    

    # @app.middleware("http")
    # async def add_process_time_header(
    #     request: Request, call_next: Callable[[Request], Awaitable[Response]]
    # ) -> Response:
    #     start_time = time.time()
    #     response = await call_next(request)
    #     process_time = time.time() - start_time
    #     response.headers["X-Process-Time"] = str(process_time)
    #     return response    