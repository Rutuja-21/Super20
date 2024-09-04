from fastapi import FastAPI, Query
from pydantic import BaseModel, Field
from typing import List, Optional
import pandas as pd
from model import recommend,output_recommended_recipes

app = FastAPI()

# Load dataset
dataset = pd.read_csv('C:/RecoMaster/Data/food1.csv')
dataset.info()


class Params(BaseModel):
    n_neighbors: int = 5
    return_distance: bool = False

class PredictionIn(BaseModel):
    nutrition_input: List[float] = Field(..., min_items=9, max_items=9)
    ingredients: List[str] = []
    params: Optional[Params] = None

class Recipe(BaseModel):
    Name: str
    CookTime: str
    PrepTime: str
    TotalTime: str
    RecipeIngredientParts: List[str]
    Calories: float
    FatContent: float
    SaturatedFatContent: float
    CholesterolContent: float
    SodiumContent: float
    CarbohydrateContent: float
    FiberContent: float
    SugarContent: float
    ProteinContent: float
    RecipeInstructions: List[str]

class PredictionOut(BaseModel):
    output: Optional[List[Recipe]] = None

    
@app.get("/")
def home():
    return {"health_check": "OK"}

@app.post("/predict/", response_model=PredictionOut)
def update_item(prediction_input: PredictionIn):
    recommendation_dataframe = recommend(
        dataset, 
        prediction_input.nutrition_input, 
        prediction_input.ingredients, 
        prediction_input.params.dict()
    )
    output = output_recommended_recipes(recommendation_dataframe)
    if output is None:
        return {"output": None}
    else:
        return {"output": output}


# If running directly, include the following line to start the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)