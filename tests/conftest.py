import os
import pytest_asyncio
from dotenv import load_dotenv

@pytest_asyncio.fixture(scope="session")
async def dependencies(request):
    args = request.config

    if args.getoption("prod"):
        load_dotenv(".env.prod")
    elif args.getoption("test"):
        load_dotenv(".env.test")
    elif args.getoption("dev"):
        load_dotenv(".env.dev")
    else:
        load_dotenv()

    # if args.getoption("sync"):
    #         os.environ["RUN_MODE"] = "SYNC"
    # else:
    #     os.environ["RUN_MODE"] = "ASYNC"

    # os.environ["DB_TYPE"] = args.getoption("db")
    # print("DB_TYPE",os.getenv("DB_TYPE"))

def pytest_addoption(parser):
    parser.addoption("--prod",action="store_true", help="Run the server in production mode.")
    parser.addoption("--test",action="store_true", help="Run the server in test mode.")
    parser.addoption("--dev",action="store_true", help="Run the server in development mode.")
    parser.addoption("--sync",action="store_true", help="Run the server in Sync mode.")
    parser.addoption("--db", help="Run the server in database type.",choices=["mysql","postgresql"], default="postgresql")