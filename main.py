#Importing FastAPI
from fastapi import FastAPI,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from pymongo import MongoClient

#Creating an Instance of FastAPI
app = FastAPI()


################################################################################
'''
->This line mounts a static file directory to a specific path in your 
FastAPI application.
->The first argument ("/static") is the path prefix where the static 
files will be served. For example, if you have a file named style.css 
in the "static" directory, it would be accessible at 
http://yourdomain.com/static/style.css.
->The StaticFiles class is used to serve static files. It takes the 
directory parameter, which specifies the path to the directory containing 
your static files. In this case, it's "static."
->The name parameter is optional and gives a name to the static files route. 
In this case, it's named "static."
'''
################################################################################
app.mount("/static", StaticFiles(directory="static"), name="static")

################################################################################
'''We are using Jinja2 templates to give an html data as a response.
We can achieve this by using jinja2 tool'''
################################################################################
templates = Jinja2Templates(directory="templates")

################################################################################
'''We are making connection to MongoDb Database->notes by using below commands'''
################################################################################

#Created User model to send data into request 
class UserDetails(BaseModel):
    userName:str
    email:str
    age:int

#Created User response model to return the result
class UserResponse(BaseModel):
    userName:str
    emails:str

################################################################################
'''This code defines a route for the root endpoint ("/"). 
When a user accesses the root URL of your API, the function 
read_root will be executed, and it returns a JSON response
{"Hello": "World"}.
'''
################################################################################
@app.get("/") #In FastAPI, @app.get is a decorator that is used to define a route for handling HTTP GET requests.
def read_root():
    return {"Hello": "World"}

################################################################################
'''This code defines a route for the endpoint "/items/{item_id}". 
It includes a path parameter item_id (an integer) and a query parameter 
q (a string or None by default). The function read_item is executed when 
a request is made to this endpoint, and it returns a JSON response containing 
the values of the path and query parameters.'''
################################################################################
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None= None):
    return {"item_id": item_id, "q": q}


#Created a post method to fetch request data and resturn respose
@app.post("/User/",response_model=UserResponse)
def createUser(user_data: UserDetails):
    return UserResponse(userName=user_data.userName, emails=user_data.email)


@app.get("/home", response_class=HTMLResponse)
async def home(request: Request):
    #docs=conn.notes.notes.find_one({})
    #print(docs)
    return templates.TemplateResponse("index.html", {"request": request})
