from fastapi import APIRouter


core_router = APIRouter()


@core_router.get("/", status_code=200)
def healthcheck():
    """[summary]
    Simple healthcheck for load balancer (Target group).
    [description]
    Return 200 for health check.
    Decorators:
        pets_router.get
    """
    return {"healthcheck": "OK"}