from fastapi.middleware.cors import CORSMiddleware

origins = [
    "http://localhost:4200",
]


def setup_cors(fastapi_app):
    fastapi_app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=["*"],
        allow_headers=["*"],
    )
