document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("task-modal");
    const openModal = document.getElementById("open-modal");
    const closeModal = document.getElementById("close-modal");
    const form = document.getElementById("task-form");
    const editForm = document.getElementById("edit-task-form");
    const editModal = document.getElementById("edit-task-modal");
    const closeEditModal = editModal.querySelector("close-modal");
    console.log(editModal.querySelector("close-modal"))
    openModal.addEventListener("click", function () {
        modal.style.display = "block";
    });

    closeModal.addEventListener("click", function () {
        modal.style.display = "none";
    })
   
    window.addEventListener("click", function (event) {
        if (event.target === modal) {
            modal.style.display = "none";
        }
    })

    form.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(form);

        fetch("/tasks/create/", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log("Server response:", data); 
            if (data.success) {
                const taskList = document.getElementById("task-list");
                const newTask = document.createElement("li");
                newTask.classList.add("task-item");
                newTask.setAttribute("data-task-id", data.task_id);
                newTask.innerHTML = `
                <strong>${data.title}</strong>
                <button class="btn-delete" data-task-id="${data.task_id}">🗑️</button>`;
                taskList.appendChild(newTask);
                
                modal.style.display = "none";
                location.reload();
            }else{
                alert("Ошибка при создании задачи");
            }
        });
    });

// delete btn func
    function addDeleteEvent(button){
        button.addEventListener("click", function (){
            const taskId = this.getAttribute("data-task-id");
            fetch(`delete_ajax/${taskId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    document.querySelector(`li[data-task-id="${taskId}"]`).remove();
                    alert("Задача удалена");
                    
                } else {
                    alert("Ошибка при удалении задачи");
                }
            });
        });
    }


    document.querySelectorAll(".btn-delete").forEach(button => {
        addDeleteEvent(button);
    });

    // Open medal edit 
    document.querySelectorAll(".btn-edit").forEach(button => {
        button.addEventListener("click", function () {
            currentTaskId = this.getAttribute("data-task-id");
            document.getElementById("edit-task-id").value = currentTaskId;
            document.getElementById("edit-title").value = this.getAttribute("data-title");
            document.getElementById("edit-description").value = this.getAttribute("data-description");
            document.getElementById("edit-category").value = this.getAttribute("data-category");
            editModal.style.display = "block";
        });
    })
    // closeEditModal.addEventListener("click", function () {
    //     editModal.style.display = "none";
    // })  

    editForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const formData = new FormData(editForm);
        formData.append("task_id", currentTaskId);
        fetch(`/tasks/edit_ajax/${currentTaskId}`, {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.success) {
                const taskItem = document.querySelector(`li[data-task-id="${currentTaskId}"]`);
                taskItem.querySelector("strong").textContent = data.title;
                taskItem.querySelector(".btn-edit").setAttribute("data-title", data.title);
                taskItem.querySelector(".btn-edit").setAttribute("data-description", data.description);
                taskItem.querySelector(".btn-edit").setAttribute("data-category", data.category);
                editModal.style.display = "none";
            } else {
                alert("Ошибка при редактировании задачи");
            }
        });
    });

    // Обработчик для пометки задачи как выполенной
    document.querySelectorAll(".btn-complete").forEach(button => {
        button.addEventListener("click", function () {
            const taskId = this.getAttribute("data-task-id");
            fetch(`/tasks/complete/${taskId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const taskItem = document.querySelector(`li[data-task-id="${taskId}"]`);
                    taskItem.querySelector(".task-title").classList.add("completed");
                    taskItem.querySelector(".btn-complete").classList.add("hidden");
                    taskItem.querySelector(".btn-incomplete").classList.remove("hidden");
                    alert("Задача помечена как выполненная");
                } else {
                    alert("Ошибка при пометке задачи как выполненной");
                }
            });
        });
    });
    // Обработчик для пометки задачи как невыполенной
    document.querySelectorAll(".btn-incomplete").forEach(button => {
        button.addEventListener("click", function () {
            const taskId = this.getAttribute("data-task-id");
            fetch(`/tasks/incomplete/${taskId}`, {
                method: "POST",
                headers: {
                    "X-CSRFToken": document.querySelector("[name=csrfmiddlewaretoken]").value,
                },
            })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    const taskItem = document.querySelector(`li[data-task-id="${taskId}"]`);
                    taskItem.querySelector(".task-title").classList.remove("completed");
                    taskItem.querySelector(".btn-complete").classList.remove("hidden");
                    taskItem.querySelector(".btn-incomplete").classList.add("hidden");
                    alert("Задача помечена как невыполненная");
                } else {
                    alert("Ошибка при пометке задачи как невыполненной");
                }
            });
        });
    });

});