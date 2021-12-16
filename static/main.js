document.querySelectorAll(".text-presentation-container input[type=\"radio\"]").forEach((ir) => {
    ir.addEventListener("change", (e) => {
        if(!e.target.checked) return;

        e.target.parentNode.parentNode.querySelector(".active").classList.remove("active");
        e.target.parentNode.parentNode.querySelector("[data-tp=\"" + e.target.value + "\"]").classList.add("active");
    });

    if(ir.checked) {
        ir.parentNode.parentNode.querySelector(".active").classList.remove("active");
        ir.parentNode.parentNode.querySelector("[data-tp=\"" + ir.value + "\"]").classList.add("active");

    }
});