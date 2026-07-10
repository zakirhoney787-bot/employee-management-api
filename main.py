from fastapi import FastAPI,HTTPException
from pydantic import BaseModel ,Field,RootModel
from typing import Annotated,Optional,List
import json

app=FastAPI()

class Employees(BaseModel):
    id: int 
    name:str
    department:str
    salary:Annotated[int,Field(..., gt=0 ,examples=[2500,12000])]
    active:bool

class EmployeeUpdate(BaseModel):
    id: Optional[int]=None
    name:Optional[str]=None
    department:Optional[str]=None
    salary:Optional[Annotated[int,Field(..., gt=0 ,examples=[2500,12000])]]=None
    active:Optional[bool]=None

def load_data():
    with open("emp.json","r") as  f:
        return json.load(f)

def save_data(data,l):
    with open("emp.json","w",encoding="utf-8") as  f:
        json.dump(data,f,indent=l)

@app.get('/employee')
def get_emp():
    data=load_data()
    return data

@app.get('/employee/{id}')
def get_emp_info(id:int):
    data = load_data()

    for employee in data:
        if employee['id']==id:
            return {
                'message':'The employees information successfully Retrieved',
                'details':employee
                    }
    else:
        raise HTTPException(status_code=404,detail="the employee id doesn't exist !")

@app.post('/Create/employee')
def create_emp(new_emp:Employees):
    model_data=new_emp.model_dump()
    data = load_data()

    for employee in data:
        if employee["id"] == model_data["id"]:
            raise HTTPException(status_code=404, detail='this id already exist !!')
    data.append(model_data)
    save_data(data,len(model_data))

    return {
        'message':'the employee is perfectly settled 😉',
        'details':model_data
        }

@app.put('/update/employee/{id}')
def update_emp(emp_update:EmployeeUpdate,id:int):
    updated_data=emp_update.model_dump(exclude_unset=True)
    data=load_data()

    for employee in data:
        if id == employee['id'] :

            for key,value in updated_data.items():
                employee[key]=value
                
            save_data(data, 4)     
            return employee
    else :
         raise HTTPException(status_code=404,detail= 'the employee id does not exist bro 🤘 ghghgh..')

@app.delete('/Delete/Employee/{id}')
def delete_emp(id :int):
    data=load_data()

    for employee in data:
        if employee['id']==id:
            data.remove(employee)
            save_data(data,4)
            
            return {
                "message":"Employee deleted"
                    }
    else:
        raise HTTPException(status_code=404,detail='This id employee does not exist  🤘 ghghgh..')

