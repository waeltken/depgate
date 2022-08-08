from typing import Union

from fastapi import FastAPI
from fastapi.responses import RedirectResponse, Response


app = FastAPI()

commit_hashes = {}


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_response():
    return {"status": "ok"}


@app.get("/status/{commit_hash}")
def read_item(commit_hash: str):
    if commit_hash in commit_hashes:
        return {"status": "green", "commit_hash": commit_hash}
    return {"status": "red", "commit_hash": commit_hash}
