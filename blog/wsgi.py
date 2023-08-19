import os

# from importlib.util import find_spec

# from fastapi import FastAPI
# from fastapi.middleware.wsgi import WSGIMiddleware
# from fastapi.staticfiles import StaticFiles

from django.core.wsgi import get_wsgi_application
from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

application = get_wsgi_application()

from blog.urls import router  # noqa

app = FastAPI(
    title="FastAPI-Djantic",
    version="1.0.0",
    description="""
    Test Driven RESTful API Specification with 
    FastApi and Djantic
    """,
    debug=True
)

# app.mount("/admin", WSGIMiddleware(application))
#
# app.mount(
#     "/static",
#     StaticFiles(
#         directory=os.path.normpath(os.path.join(
#             find_spec("django.contrib.admin").origin,
#             "..", "static"))), name="static",
# )

# app.add_middleware(
#     CORSMiddleware,
#     allow_origin=['*'],
#     allow_credentials=True,
#     allow_methods=['*'],
#     allow_headers=['*']
# )

app.include_router(router=router, prefix='/api/v1')
