from pathlib import Path

import click
import uvicorn
from fastapi import FastAPI
from web_api.routers import hierarchy

app = FastAPI()

# Registers routers
app.include_router(hierarchy.router)


@click.command(name='plot')
@click.option('--host', "host", type=click.STRING, default="127.0.0.1", help="Host where the server is running")
@click.option('--port', "port", type=click.INT, default=8000, help="Listening port")
def main(host: str, port: int):
    """
    Ex. PYTHONPATH=. python dev_run.py --host 172.21.0.1 --port 5000
    """
    reload_dirs = [str(Path(__file__).absolute().parent)]
    uvicorn.run(
        "web_api.server:app",
        host=host,
        port=port,
        log_level="info",
        reload=True,
        reload_dirs=reload_dirs
    )


if __name__ == "__main__":
    main()
