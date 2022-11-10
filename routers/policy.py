from fastapi import APIRouter, HTTPException
import hashlib
import json
import os.path

router = APIRouter()

class PolicyManager:
    def __init__(self):
        self.policy_location = "./policies"

    def make_path(self, name):
        return os.path.join(self.policy_location, name +".json")

    def make_error(self, name, msg):
        return {
            "desc":"Policy Server Error [PSE]",
            "msg":msg,
            "device_id":name
        }

    def hash_policy(self, name):
        try:
            h = hashlib.sha256()
            with open(self.make_path(name), "rb") as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    h.update(chunk)
            return (200, h.hexdigest())
        except:
            return (404, self.make_error(name, "POLICY_NOT_FOUND"))

    def load_policy(self, name):
        try:
            with open(self.make_path(name), "r") as f:
                d = f.read()
                return (200, json.loads(d))
        except:
            return (404, self.make_error(name, "POLICY_NOT_FOUND"))

pm = PolicyManager()

@router.get("/policy/{device_id}/")
async def get_policy(device_id: str):
    status, data = pm.load_policy(device_id)

    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    else:
        return data

@router.get("/policy/check/{device_id}/")
async def check_policy(device_id: str):
    status, data = pm.hash_policy(device_id)

    if status != 200:
        raise HTTPException(status_code=status, detail=data)
    else:
        return {
            "device_id":device_id,
            "hash": data
        }

