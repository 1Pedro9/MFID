
function route(e, path) {
    document.querySelectorAll(".route button").forEach(object => {
        object.classList.remove("route-chosen");
    });
    e.classList.add("route-chosen");
    document.querySelectorAll(".settings section").forEach(object => {
        object.classList.remove("chosen");
    });
    document.querySelector(".settings ." + path).classList.add("chosen");
}