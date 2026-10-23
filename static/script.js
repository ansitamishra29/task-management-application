
async function addTask() {
    const taskInput = document.getElementById("taskInput");
    const taskText = taskInput.value.trim();

    if (taskText === "") {
        alert("Please enter a task!");
        return;
    }

    try {
        const response = await fetch("/add-task", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ title: taskText })
        });

        if (!response.ok) {
            throw new Error("Could not save task.");
        }

        const task = await response.json();
        displayTask(task);
        taskInput.value = "";
    } catch (error) {
        alert("Could not save the task. Please check that Flask is running.");
        console.error(error);
    }
}

function displayTask(task) {
    const taskList = document.getElementById("taskList");
    const listItem = document.createElement("li");

    const taskLabel = document.createElement("span");
    taskLabel.textContent = task.title;

    if (task.status === "completed") {
        taskLabel.style.textDecoration = "line-through";
    }

    const completeButton = document.createElement("button");
    completeButton.textContent =
        task.status === "completed" ? "Undo" : "Complete";

    // Update task status in MySQL
    completeButton.onclick = async function () {
        const isCompleted =
            taskLabel.style.textDecoration === "line-through";

        const newStatus = isCompleted ? "pending" : "completed";

        try {
            const response = await fetch(`/update-task/${task.id}`, {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({ status: newStatus })
            });

            if (!response.ok) {
                throw new Error("Could not update task.");
            }

            task.status = newStatus;

            if (newStatus === "completed") {
                taskLabel.style.textDecoration = "line-through";
                completeButton.textContent = "Undo";
            } else {
                taskLabel.style.textDecoration = "none";
                completeButton.textContent = "Complete";
            }
        } catch (error) {
            alert("Could not update task status.");
            console.error(error);
        }
    };

    // Delete button (currently removes from page only)
    const deleteButton = document.createElement("button");
    deleteButton.textContent = "Delete";

    
deleteButton.onclick = async function () {
    const confirmDelete = confirm("Are you sure you want to delete this task?");

    if (!confirmDelete) {
        return;
    }

    try {
        const response = await fetch(`/delete-task/${task.id}`, {
            method: "DELETE"
        });

        if (!response.ok) {
            throw new Error("Could not delete task.");
        }

        listItem.remove();
    } catch (error) {
        alert("Could not delete the task. Please try again.");
        console.error(error);
    }
};


    listItem.appendChild(taskLabel);
    listItem.appendChild(completeButton);
    listItem.appendChild(deleteButton);

    taskList.appendChild(listItem);
}

// Load saved tasks from MySQL
async function loadTasks() {
    try {
        const response = await fetch("/get-tasks");

        if (!response.ok) {
            throw new Error("Could not load tasks.");
        }

        const tasks = await response.json();

        const taskList = document.getElementById("taskList");
        taskList.innerHTML = "";

        tasks.forEach(function (task) {
            displayTask(task);
        });
    } catch (error) {
        console.error("Error loading tasks:", error);
    }
}

document.addEventListener("DOMContentLoaded", loadTasks);
