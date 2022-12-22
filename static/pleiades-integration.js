if(pleiades = document.querySelector('[data-ext-hint=pleiades]')) {
    pleiades_id = document.querySelector('[name=pleiades_id]')
    pleiades_lat = document.querySelector('[name=coordinates_lat]')
    pleiades_long = document.querySelector('[name=coordinates_long]')

    query_interface = document.createElement('div');
    query_interface.classList.add('pleiades-ui')
    query_interface.innerHTML =
    `<button type="button" data-pleiades-ref="sync">LOAD from Pleiades</button>`;
    pleiades.after(query_interface);

    pleiades_query_button = query_interface.querySelector('[data-pleiades-ref="sync"]');

    pleiades_query_button.addEventListener("click", (e) => {
        key = pleiades_id.value;

        fetch('http://pleiades.stoa.org/places/' + key + '/json')
            .then(response => response.json())
            .then(result => {
                pleiades_long.value = result['reprPoint'][0];
                pleiades_lat.value = result['reprPoint'][1];
            })
            .catch(error => {
                alert("ERROR using Pleiades integration, please retry.\n\nmessage:" + error);
            });
    });
}