import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime, timezone

from database import db, create_document, get_documents
from schemas import BlogPost, Confession

app = FastAPI(title="Scrapp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Scrapp backend is alive"}

@app.get("/api/hello")
def hello():
    return {"message": "Hello from Scrapp API!"}

@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    # Ensure env flags
    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Blog endpoints
@app.post("/api/blogs", response_model=dict)
def create_blog(post: BlogPost):
    try:
        inserted_id = create_document("blogpost", post)
        return {"id": inserted_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/blogs", response_model=List[dict])
def list_blogs(limit: Optional[int] = 20):
    try:
        docs = get_documents("blogpost", limit=limit)
        # Normalize ObjectId and timestamps
        result = []
        for d in docs:
            d["id"] = str(d.pop("_id", ""))
            for t in ["created_at", "updated_at"]:
                if d.get(t) and isinstance(d[t], datetime):
                    d[t] = d[t].astimezone(timezone.utc).isoformat()
            result.append(d)
        # Sort latest first
        result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Confession endpoints
@app.post("/api/confessions", response_model=dict)
def create_confession(item: Confession):
    try:
        inserted_id = create_document("confession", item)
        return {"id": inserted_id, "status": "created"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/confessions", response_model=List[dict])
def list_confessions(limit: Optional[int] = 30):
    try:
        docs = get_documents("confession", limit=limit)
        result = []
        for d in docs:
            d["id"] = str(d.pop("_id", ""))
            for t in ["created_at", "updated_at"]:
                if d.get(t) and isinstance(d[t], datetime):
                    d[t] = d[t].astimezone(timezone.utc).isoformat()
            result.append(d)
        result.sort(key=lambda x: x.get("created_at", ""), reverse=True)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
