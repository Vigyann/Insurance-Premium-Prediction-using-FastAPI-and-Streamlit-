from fastapi import FastAPI
from pydantic import BaseModel,Field,computed_field
from typing import Literal,Annotated
import pickle 
import pandas as pd
from fastapi.responses import JSONResponse

with open('model.pkl','rb') as f:
    model=pickle.load(f)

app=FastAPI()

tier_1_cities = ["Mumbai", "Delhi", "Bangalore", "Chennai", "Kolkata", "Hyderabad", "Pune"]
tier_2_cities = [
    "Jaipur", "Chandigarh", "Indore", "Lucknow", "Patna", "Ranchi", "Visakhapatnam", "Coimbatore",
    "Bhopal", "Nagpur", "Vadodara", "Surat", "Rajkot", "Jodhpur", "Raipur", "Amritsar", "Varanasi",
    "Agra", "Dehradun", "Mysore", "Jabalpur", "Guwahati", "Thiruvananthapuram", "Ludhiana", "Nashik",
    "Allahabad", "Udaipur", "Aurangabad", "Hubli", "Belgaum", "Salem", "Vijayawada", "Tiruchirappalli",
    "Bhavnagar", "Gwalior", "Dhanbad", "Bareilly", "Aligarh", "Gaya", "Kozhikode", "Warangal",
    "Kolhapur", "Bilaspur", "Jalandhar", "Noida", "Guntur", "Asansol", "Siliguri"
]

class userinput(BaseModel):

    age: Annotated[int,Field(...,gt=0,lt=120,description='Age of the user')]
    weight:Annotated[float,Field(...,gt=0,description='Weight of the user')]
    height:Annotated[float,Field(...,gt=0,lt=2.5,description='Age of the User')]
    income_lpa:Annotated[float,Field(...,gt=0,description='Annual salary of the user')]
    smoker:Annotated[bool,Field(...,description='Is a smoker')]
    city:Annotated[str,Field(...,description='Enbter the name ogf the city')]
    occupation: Annotated[Literal['retired', 'freelancer', 'student', 'government_job',
       'business_owner', 'unemployed', 'private_job'],Field(...,description='ocuupation of the user')]
    
    
    @computed_field
    @property
    def bmi(self)->float:
        return self.weight / (self.height**2)
    
    @computed_field
    @property
    def lifestyle_risk (self) -> str:
       if self.smoker and self.bmi >30:
           return "high"
       elif self.smoker and self.bmi >27:
           return "medium"
       else:
           return "low"
       
    @computed_field
    @property
    def age_group(self) ->str:
      if self.age<25:
        return "Young"
      elif self.age<45:
        return "adult"
      elif self.age <60:
        return "middle_aged"
      return "senior"
    
    @computed_field
    @property
    def city_tier(self)-> int:
      if self.city in tier_1_cities:
        return 1
      elif self.city in tier_2_cities:
        return 2
      else:
        return 3

@app.get('/')
def home():
   return {'message':'Insurance Premium Prediction API'}

@app.get('/')
def health_check():
   return{
      'status':'OK'
   }

classes=model.classes_.tolist()
@app.post('/predict')
def predict_premium(data: userinput):

       
       input_df=pd.DataFrame([{
          'bmi':data.bmi,
          'age_group':data.age_group,
          'lifestyle_risk':data.lifestyle_risk,
          'city_tier':data.city_tier,
          'income_lpa':data.income_lpa,
          'occupation':data.occupation
       }
       ])

       prediction=model.predict(input_df)[0]
       probabilities=model.predict_proba(input_df)[0]
       confidence=max(probabilities)
       class_probabs=dict(zip(classes,map(lambda p:round(p,4),probabilities)))
       
       return JSONResponse(status_code=200,content={'predicted_category':prediction,'confidence':round(confidence,4),'class_probabilities':class_probabs})
      
       
       





