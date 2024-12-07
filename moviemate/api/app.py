import sys
import os

sys.path.append(os.path.abspath('..'))

from fastapi import FastAPI, HTTPException
from modules.adaptive.filters.collaborative import CollaborativeFiltering
from modules.adaptive.filters.content_based import ContentBasedRecommender
from modules.adaptive.filters.cold_start import ColdStartRecommender

app = FastAPI()

cf_model = CollaborativeFiltering('../storage/u.data', '../storage/u.item')
cb_model = ContentBasedRecommender('../storage/u.item')
cold_start_model = ColdStartRecommender('../storage/u.item')


@app.post("/users")
def add_user(user_id: int):
    # Add logic to handle user addition (e.g., save to a database)
    return {"message": f"User {user_id} added successfully."}


@app.post("/users/login")
def login_user(user_id: int):
    # Add logic for authentication (e.g., check user exists in database)
    return {"message": f"User {user_id} logged in successfully."}


@app.get("/recommendations")
def get_recommendations(user_id: int):
    if not user_id:
        raise HTTPException(status_code=400, detail="User ID is required.")
    
    recommendations = cf_model.recommend(user_id)
    if not recommendations:
        recommendations = cold_start_model.get_recommendations()
    
    return {"user_id": user_id, "recommendations": recommendations}
