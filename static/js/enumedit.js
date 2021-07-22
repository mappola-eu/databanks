document.querySelectorAll(".modal-toggle").forEach( (mt) => {
    mt.addEventListener("click", (e) => {
        document.querySelector(e.target.getAttribute("data-modal")).classList.toggle("__visible");
        e.preventDefault();
    } );
} );

document.querySelectorAll(".edit-enum-link").forEach( (mt) => {
    mt.addEventListener("click", (e) => {
        document.querySelector(e.target.getAttribute("data-modal")).querySelector("iframe").setAttribute("src", e.target.getAttribute("href"));
        setTimeout(() => {
            document.querySelector(e.target.getAttribute("data-modal")).classList.toggle("__visible");
        }, 150);
        e.preventDefault();
    } );
} );