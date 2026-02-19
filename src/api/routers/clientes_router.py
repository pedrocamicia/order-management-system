from fastapi import APIRouter

router = APIRouter(tags=["Cllientes"])

service = None
def set_service(_service):
    global service
    service = _service
    

