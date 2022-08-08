from fastapi import FastAPI, Depends, status, Query, HTTPException, Path
from fastapi.responses import RedirectResponse
from fastapi.security import APIKeyHeader


app = FastAPI()

api_keys = ["super-secret-token"]

commit_hashes = {}
api_key_header = APIKeyHeader(name="Authorization")


def api_key_auth(api_key: str = Depends(api_key_header)):
    if api_key not in api_keys:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Incorrect API key"
        )
    return api_key


@app.get("/")
def redirect_to_docs():
    return RedirectResponse(url="/docs")


@app.get("/health")
def health_response():
    return {"status": "ok"}


@app.get("/status/{commit_hash}")
def read_item(commit_hash: str = Path(min_length=40, max_length=40)):
    if commit_hash in commit_hashes:
        return {"status": commit_hashes[commit_hash], "commit_hash": commit_hash}
    return {"status": "red", "commit_hash": commit_hash}


@app.put("/status/{commit_hash}", dependencies=[Depends(api_key_auth)])
def write_status(commit_hash: str, status: str = "green"):
    commit_hashes[commit_hash] = status
    return {"status": status, "commit_hash": commit_hash}
