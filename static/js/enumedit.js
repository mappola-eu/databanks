document.querySelectorAll(".modal-toggle").forEach( (mt) => {
    mt.addEventListener("click", async (e) => {
        e.preventDefault();

        const MODAL = document.querySelector(e.target.getAttribute("data-modal"));
        
        if(MODAL.hasAttribute("data-enum-key")) {
            const key = MODAL.getAttribute("data-enum-key");
            const list = document.querySelector(MODAL.getAttribute("data-enum-list"));

            json_data = await fetch(key);
            data = await json_data.json();

            current_values = list.value;
            list.innerHTML = "";

            for (const item of data.data) {
                el = document.createElement("option")
                el.value = item[0];
                el.innerText = item[1];
                list.appendChild(el);
            }

            list.value = current_values;
        }
        
        MODAL.classList.toggle("__visible");
    } );
} );

document.querySelectorAll(".edit-enum-link").forEach( (mt) => {
    mt.addEventListener("click", async (e) => {
        e.preventDefault();

        const BASE_URL = e.target.getAttribute("href");
        const MODAL = document.querySelector(e.target.getAttribute("data-modal"));

        MODAL.querySelector("iframe").setAttribute("src", BASE_URL);
        setTimeout(() => {
            MODAL.classList.toggle("__visible");
        }, 150);

        console.log(e.target.previousSibling);
        console.log(e.target);

        MODAL.setAttribute("data-enum-list", '#' + e.target.parentNode.querySelector("select").getAttribute("id"));
        MODAL.setAttribute("data-enum-key", BASE_URL + '/api');
    } );
} );