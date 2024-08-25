from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.company.companyController import companyRouter
from app.user.userController import userRouter
from app.results.resultsController import resultsRouter
from app.resultsListening.resultsListeningController import resultsListeningRouter
from app.resultsSpeaking.resultsSpeakingController import resultsSpeakingRouter
from app.resultsWriting.resultsWritingController import resultsWritingRouter
from app.auth.authController import authRouter

description = """
All these configurations are suggested in the doc and
are used in the OpenAPI specification and the automatic API docs UIs.

This is a test of the description. 🚀
"""
app = FastAPI(
    title='Deepvoice English API',
    description=description,
    version='0.0.1',
    summary='REST API for deepvoice english'
)

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter()

app.include_router(companyRouter)
app.include_router(userRouter)
app.include_router(resultsRouter)
app.include_router(resultsListeningRouter)
app.include_router(resultsSpeakingRouter)
app.include_router(resultsWritingRouter)
app.include_router(authRouter)
