import datetime

stored_tasks = {}
x = datetime.datetime.now()
print("TO DO APP.")
while True:
    task = input("Enter the name of the task: ")
    description = input("Add description of the task: ")
    if input("Do you want to add a timer? Y/N: ".lower()) == "y":
        set_time = input("Until what time?: ")

    stored_tasks[task] = {
        "description": description,
        "date": x.strftime("%c"),
        "timer": set_time,
    }
    taskCount = 0
    for i, (task_name, task_data) in enumerate(stored_tasks.items()):
        print(i, task_name)
        print(task_data["description"])
        print(task_data["date"])
        print(task_data["timer"])
        taskCount = i + 1
    choice = input(
        f"Select task to see(1-{taskCount})\nor type 'add' to add a new task: "
    ).lower()
    if choice == "add":
        continue
    task = list(stored_tasks)[int(choice) - 1]
    description = list(stored_tasks.values())[int(choice) - 1]
    print(f"The task is {task}\nand description is {description}")
    print(stored_tasks)
    if input("Add new task?(y/n): ").lower() == "n":
        break
print("bye")
