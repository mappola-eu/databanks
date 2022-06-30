if(zotero = document.querySelector('[data-ext-hint=zotero]')) {
    query_interface = document.createElement('div');
    query_interface.classList.add('zotero-ui')
    query_interface.innerHTML =
    `<h3>Load from Zotero</h3>
    <div class="zotero-col">
        <h4>Search for existing</h4>
        <input data-zotero-ref="query.title" type="search" preview="write search term; then press enter">
        <select data-zotero-ref="query.output" disabled>
        </select>
        <button type="button" data-zotero-ref="query.use" disabled>use selected</button>
    </div>
    <div class="zotero-col">
        <h4>Create new</h4>
        <input data-zotero-ref="new.title" preview="title">
        <select data-zotero-ref="new.type">
            <option disabled selected>choose a type</option>
        </select>
        <button type="button" data-zotero-ref="new">create</button>
    </div>`;
    zotero.prepend(query_interface);

    zotero_query_title = zotero.querySelector('[data-zotero-ref="query.title"]');
    zotero_query_output = zotero.querySelector('[data-zotero-ref="query.output"]');
    zotero_query_use = zotero.querySelector('[data-zotero-ref="query.use"]');
    zotero_new_title = zotero.querySelector('[data-zotero-ref="new.title"]');
    zotero_new_type = zotero.querySelector('[data-zotero-ref="new.type"]');
    zotero_new = zotero.querySelector('[data-zotero-ref="new"]');

    inscription_reference_comment = document.querySelector("#Inscriptions-reference_comment");
    inscription_zotero_item_id = document.querySelector("#Inscriptions-zotero_item_id");

    fetch('/ext/zotero/quickadd/types')
        .then(response => response.json())
        .then(result => {
            for (const type of result.items) {
                let option_field = document.createElement("option");
                option_field.value = type.itemType;
                option_field.innerText = type.localized;
                zotero_new_type.appendChild(option_field);
            }
        })
        .catch(error => {
            alert("ERROR loading Zotero integration, please retry.\n\nmessage:" + error)
        });
    
    zotero_query_title.addEventListener("keypress", (e) => {
        const ENTER_KEY = 13;
        if (e.which == ENTER_KEY) {
            e.preventDefault();
            e.stopPropagation();

            query = zotero_query_title.value;
            zotero_query_title.setAttribute("disabled", true)
            fetch('/ext/zotero/query?for=' + query)
                .then(response => response.json())
                .then(result => {
                    zotero_query_title.removeAttribute("disabled");

                    if(result.found > 0) {
                        zotero_query_use.removeAttribute("disabled");
                        zotero_query_output.removeAttribute("disabled");
                    } else {
                        zotero_query_use.setAttribute("disabled", true);
                        zotero_query_output.setAttribute("disabled", true);
                    }
                    zotero_query_output.innerHTML = "";
    
                    for (const item of result.items) {
                        let option_field = document.createElement("option");
                        option_field.value = item.key;
                        option_field.innerText = item.title + " (" + item.authors + ")";
                        zotero_query_output.appendChild(option_field);
                    }
                })
                .catch(error => {
                    zotero_query_title.removeAttribute("disabled");
                    alert("ERROR using Zotero integration, please retry.\n\nmessage:" + error);
                });
        }
    });

    zotero_query_use.addEventListener("click", (e) => {
        key = zotero_query_output.value;
        if(!key) return;

        fetch('/ext/zotero/fetch/' + key)
            .then(response => response.json())
            .then(result => {
                const response = result.items[0];
                let creator_length = response.data.creators.length;
                let creator_string;
                if (creator_length == 1) {
                    creator_string = response.data.creators[0].firstName + " " + response.data.creators[0].lastName
                } else {
                    creator_string = response.data.creators[0].firstName + " " + response.data.creators[0].lastName + " et al.";
                }
                inscription_zotero_item_id.value = response.key;
                inscription_reference_comment.value = 
                    creator_string + ", " +
                    response.data.date + ": " +
                    response.data.title;
            })
            .catch(error => {
                alert("ERROR using Zotero integration, please retry.\n\nmessage:" + error);
            });
    });

    zotero_new.addEventListener("click", (e) => {
        title = zotero_new_title.value;
        type = zotero_new_type.value;
        if(!title || !type) return;

        const data = new URLSearchParams();
        data.append('title', title);

        fetch('/ext/zotero/quickadd/of/type/' + type, { method: 'post', body: data })
            .then(response => response.json())
            .then(result => {
                const key = result.items[0].key;
                inscription_zotero_item_id.value = key;
                inscription_reference_comment.value = title;
            })
            .catch(error => {
                alert("ERROR using Zotero integration, please retry.\n\nmessage:" + error);
            });
    });
}