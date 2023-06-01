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
    </div>
    <div class="zotero-col">
        <h4>Synchronize</h4>
        <p>(when reference settings in Zotero have changed)</p>
        <button type="button" data-zotero-ref="sync">update now</button>
    </div>`;
    zotero.prepend(query_interface);

    zotero_query_title = zotero.querySelector('[data-zotero-ref="query.title"]');
    zotero_query_output = zotero.querySelector('[data-zotero-ref="query.output"]');
    zotero_query_use = zotero.querySelector('[data-zotero-ref="query.use"]');
    zotero_new_title = zotero.querySelector('[data-zotero-ref="new.title"]');
    zotero_new_type = zotero.querySelector('[data-zotero-ref="new.type"]');
    zotero_new = zotero.querySelector('[data-zotero-ref="new"]');
    zotero_sync = zotero.querySelector('[data-zotero-ref="sync"]');

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
            .then(updateCitation)
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

    zotero_sync.addEventListener("click", (e) => {
        key = inscription_zotero_item_id.value;

        fetch('/ext/zotero/fetch/' + key)
            .then(response => response.json())
            .then(updateCitation)
            .catch(error => {
                alert("ERROR using Zotero integration, please retry.\n\nmessage:" + error);
            });
    });

    const updateCitation = (result) => {
        const response = result.items[0];
        let authors = filterCreatorFor(response.data.creators, "author");
        let creator_string = makeCreatorString(authors)

        citation = creator_string + ", " + response.data.title

        if (response.data.itemType == "journalArticle") {
            let journal = response.data.journalAbbreviation || response.data.publicationTitle
            let edition = response.data.issue
            let date = response.data.date
            let pages = response.data.pages

            citation += ", " + journal + " " + edition + " (" + date + "), " + pages + "."
        } else if (response.data.itemType == "book") {
            let place = response.data.place
            let date = response.data.date
            citation += ", " + place + " " + date + "."
        } else if (response.data.itemType == "bookSection") {
            let bookTitle = response.data.bookTitle
            let editors = makeCreatorString(filterCreatorFor(response.data.creators, "editor"), " (ed.)")
            let place = response.data.place
            let date = response.data.date
            let pages = response.data.pages
            citation += ". In: " + editors + ", " + bookTitle + ", " + place + " " + date
            if (pages) citation += ", " + pages
            citation += "."
        }

        console.log(response.data)
        inscription_zotero_item_id.value = response.key;
        inscription_reference_comment.value = citation;
    }

    const filterCreatorFor = (creators, filter) => {
        return creators.filter((i) => {
            return i.creatorType == filter
        })
    }

    const optconc = (a, b) => {
        if(a) return a + b
        return ""
    }

    const makeCreatorString = (creators, prefix) => {
        let creators_length = creators.length;
        if (creators_length == 1) {
            creator_string = optconc(creators[0].firstName[0], ". ") + creators[0].lastName
            if (prefix) creator_string += prefix
        } else if (creators_length >= 2) {
            creator_string = optconc(creators[0].firstName[0], ". ") + creators[0].lastName
            if (prefix) creator_string += prefix
            creator_string += ", "
            creator_string += optconc(creators[0].firstName[0], ". ") + creators[1].lastName
            if (prefix) creator_string += prefix

            if (creators_length >= 3) {
                creator_string += " et al."
            }
        }

        return creator_string
    }
}