import json
import argparse
import os
import datetime

# Save function
def save():
    with open(name_tracker, 'w') as archivo:
        json.dump(js, archivo, indent=4)

# Add function
def add(desc:  str):
    if js:  # Si existe entonces buscamos el mayor indice
        indice = max(int(key) for key in js.keys())
    else:  # Sino, comenzamos en 0
        indice = 0

    id = indice+1
    js[id] = {"desc":desc,
           "status":"Todo",
            "createdAt":str(datetime.datetime.now().date()),
            "updatedAt":0
            }

    print(f"Task added successfully (ID: {id})")
    # Save
    save()

# Update
def update(id:str, new_desc:str):
    try:
        old_desc = js[id]["desc"]
        js[id]["desc"] = new_desc
        js[id]["updatedAt"] = str(datetime.datetime.now().date())
        print("Description changed:")
        print(f"'{old_desc}'\nto\n'{new_desc}'")
        # Guardamos
        save()
    except KeyError:
        print("Task not found")

# Delete
def delete(id:str):
    try:
        info = js[id]["desc"]
        del js[id]
        print(f"Deleted task {id} with description: {info}")
        save()
    except KeyError:
        print("Task not found")

#mark in progresss
def mark_in_progress(id:str):
    try:
        js[id]["status"] = "In progress"
        print(f"Task {id} is in progress now!")
        save()
    except KeyError:
        print("Task not found")


# Mark done
def mark_done(id: str):
    try:
        js[id]["status"] = "Done"
        print(f"Task {id} is done now!")
        save()
    except KeyError:
        print("Task not found")


# List
def listar(mode="All"):

    if mode == "In-progress":
        for number,info in js.items():
            if js[number]["status"] == "In progress":
                print(f"{number}: {info['desc']} ({info['status']})")
    elif mode == "Todo":
        for number,info in js.items():
            if js[number]["status"] == "Todo":
                print(f"{number}: {info['desc']} ({info['status']})")
    elif mode == "Done":
        for number,info in js.items():
            if js[number]["status"] == "Done":
                print(f"{number}: {info['desc']} ({info['status']})")

    elif mode =="All":
        for number,info in js.items():
            print(f"{number}: {info['desc']} ({info['status']})")


if __name__ == "__main__":
    name_tracker = "tracker.json"  # Nombre predeterminado

    # Creamos diccionario del json
    if os.path.exists(name_tracker):  # Si ya existe lo cargamos
        with open(name_tracker, "r") as file:
            js = json.load(file)
    else:
        with open(name_tracker, "w") as file:  # Si no existe creamos el diccionario
            js = {}

    # Parser
    parser = argparse.ArgumentParser(description="ClI Tracker")
    # Arguments
    parser.add_argument("-A","--add", type=str, help="Add a task")
    parser.add_argument("-U","--update", type=str,nargs=2, metavar=('Task_id', 'Desc'), help="Update a task")
    parser.add_argument("-D","--delete", type=str, help="Delete a task")
    parser.add_argument("-I","--inprogress", type=str, help="Mark like 'in progress' that task")
    parser.add_argument("--done", type=str, help="Mark like 'done' that task")
    parser.add_argument("-L",'--listar',type=str,choices=['Done', 'Todo', 'In-progress', "All"],
                                    default='All',help='List tasks')
    args = parser.parse_args()

# Arguments
    if args.add:
        add(args.add)
    elif args.update:
        update(args.update[0], args.update[1])
    elif args.delete:
        delete(args.delete)
    elif args.inprogress:
        mark_in_progress(args.inprogress)
    elif args.done:
        mark_done(args.done)
    elif args.listar:
        listar(args.listar)

