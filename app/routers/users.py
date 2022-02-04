from fastapi import APIRouter, Depends, HTTPException
from ..dependencies import get_token_header
from ..database import users_coll
from ..database.models import SimpleUser, User  


router = APIRouter(
    prefix="/users",
    tags=["users"],
    # dependencies=[Depends(get_token_header)],
    responses={404: {"description": "Not found"}},
)


# Create
@router.post("/")
async def create_user(user: User):
    found_user = users_coll.find_one({"username": user.username})
    if found_user is not None:
        found_user["_id"] = str(found_user["_id"])
        return found_user
    res = users_coll.insert_one(user.dict())
    user = user.dict()
    user["id"] = str(res.inserted_id)
    return user


# Retreive
@router.get("/", tags=["users"])
async def read_users():
    results = [ user for user in users_coll.find() ]
    for idx, user in enumerate(results):
        results[idx]["_id"] = str(user["_id"])
    return results

@router.get("/{username}")
async def read_user(username: str):
    results = users_coll.find_one({"username": username})
    if results is not None:
        results["_id"] = str(results.get("_id",""))
        return results  
    raise HTTPException(status_code=404, detail="user not found")


# Update
@router.put("/")
async def update_user(user: User):
    found_user = users_coll.find_one({"username": user.username})
    if found_user is not None:
        users_coll.update_one({"username": user.username},{"$set": user.dict()})
        return {"details": f"user '{user.username}' updated"}
    raise HTTPException(status_code=404, detail="user not found")


# Delete
@router.delete("/")
async def create_user(user: SimpleUser):
    found_user = users_coll.find_one({"username": user.username})
    if found_user is not None:
        users_coll.delete_one({"username":user.username})
        return {"details": f"user '{user.username}' deleted"}
    raise HTTPException(status_code=404, detail="user not found")
