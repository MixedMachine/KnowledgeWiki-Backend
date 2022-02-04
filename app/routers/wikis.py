from fastapi import APIRouter, Depends, HTTPException

from ..database import users_coll, wikis_coll
from ..database.models import SimpleUser, Wiki, SimpleWiki

router = APIRouter(
    prefix="/wiki",
    tags=["wiki"],
    responses={404: {"description": "Not found"}},
)


# Create
@router.post("/")
async def create_wiki(wiki: Wiki):
    user = users_coll.find_one({"username": wiki.user})
    if user is None:
        raise HTTPException(status_code=404, detail="user not found")
    found_wiki = wikis_coll.find_one({"topic": wiki.topic, "user": wiki.user})
    if found_wiki is not None:
        found_wiki["_id"] = str(found_wiki["_id"])
        return found_wiki
    res = wikis_coll.insert_one(wiki.dict())
    wiki = wiki.dict()
    wiki["id"] = str(res.inserted_id)
    return wiki


# Retreive
@router.get("/")
async def read_wikis(user: SimpleUser):
    results = [ wiki for wiki in wikis_coll.find({"user": user.username}) ]
    for idx, wiki in enumerate(results):
        results[idx]["_id"] = str(wiki["_id"])
    return results

@router.get("/page")
async def read_wiki(wiki: SimpleWiki):
    results = wikis_coll.find_one({"user": wiki.user, "topic": wiki.topic})
    if results is not None:
        results["_id"] = str(results.get("_id",""))
        return results  
    raise HTTPException(status_code=404, detail="wiki not found")


# Update
@router.put("/")
async def update_wiki(wiki: Wiki):
    found_wiki = wikis_coll.find_one({"topic": wiki.topic})
    if found_wiki is not None:
        wikis_coll.update_one({"topic": wiki.topic},{"$set": wiki.dict()})
        return {"details": f"wiki '{wiki.topic}' updated"}
    raise HTTPException(status_code=404, detail="wiki not found")


# Delete
@router.delete("/")
async def create_wiki(wiki: SimpleWiki):
    found_wiki = wikis_coll.find_one({"topic": wiki.topic, "user": wiki.user})
    if found_wiki is not None:
        wikis_coll.delete_one({"topic":wiki.topic})
        return {"details": f"wiki '{wiki.topic}' deleted"}
    raise HTTPException(status_code=404, detail="wiki not found")
