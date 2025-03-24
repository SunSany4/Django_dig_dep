document.addEventListener("DOMContentLoaded", function () {
    const modal = document.getElementById("task-modal");
    const openModal = document.getElementById("open-modal");
    const closeModal = document.getElementById("close-modal");
    const form = document.getElementById("task-form");
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




    form.addEventListener("submit", function (event) {
        event.preventDefault();

        const formData = new FormData(form);

        fetch("{% url 'create_task' %}", {
            method: "POST",
            body: formData,
            headers: {
                "X-CSRFToken": document.querySelector('[name=csrfmiddlewaretoken]').value
            },
    })
.then(response => response.json())
.then(data => {
    if (data.success) {
        modal.style.display = "none";
        location.reload();
    }else{
        alert("Ошибка при создании задачи");
    }
})
    });
});