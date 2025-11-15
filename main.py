from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from models import Todo_ModelFormat

app = FastAPI()


@app.get("/hello")
async def root():
    return {"message": "Hi there!"}

todo_list = []

#create todo
@app.post("/todos")                                                     ##endpoint to create a new todo
async def create_todo(todo: Todo_ModelFormat):                          ##function to handle the creation of a new todo
    todo_list.append(todo)
    return {"message": "Todo created successfully"}

#get all todos
@app.get("/todos")
async def get_todos():
    return {"todos": todo_list}

#get single todo
@app.get("/todos/{todo_id}")
async def get_todo(todo_id: int):
    for todo in todo_list:
        if todo.id == todo_id:
            return {"todo": todo}
    return {"message": "Todo not found"}

#update todo
@app.put("/todos/{todo_id}")
async def update_todo(todo_id: int, updated_todo: Todo_ModelFormat):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            todo_list[index] = updated_todo
            return {"message": "Todo updated successfully"}
    return {"message": "Todo not found"}

#delete todo
@app.delete("/todos/{todo_id}")
async def delete_todo(todo_id: int):
    for index, todo in enumerate(todo_list):
        if todo.id == todo_id:
            del todo_list[index]
            return {"message": "Todo deleted successfully"}
    return {"message": "Todo not found"}

##
