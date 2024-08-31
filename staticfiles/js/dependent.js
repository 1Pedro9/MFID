
document.querySelectorAll(".dependent-list li").forEach(object => {
    const a = object.querySelector(".dependent-container");
    if (a.style.display == "") {
        a.style.display = "None";
    }
    object.addEventListener("click", function () {

        a.style.display = a.style.display == "none" ? "block" : "none";
        console.log(a)
    });
});