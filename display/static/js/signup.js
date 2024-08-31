const list = ['personal', 'conditions', 'allergies', 'medicine', 'mainmember', 'dependents']

function back() {
    count -= 1;
    if (count < 0) {
        count = 0;
    }
    update();
}

function next() {
    count += 1;
    if (count >= list.length) {
        window.location.href = "{% url 'index' %}";
    }
    update();
}

function update() {
    document.querySelectorAll(".login section").forEach(object => {
        object.classList.remove("chosen");
    });
    document.querySelector(".login ." + list[count]).classList.add("chosen");
}