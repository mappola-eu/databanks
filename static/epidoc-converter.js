if(epidoc_btn = document.querySelector('[data-ext-hint=epidoc-btn]')) {
    epidoc_target = document.querySelector('[data-ext-hint=epidoc-target]')
    epidoc_source = document.querySelector('[data-ext-hint=epidoc-source]')

    // We do not use JQuery, but we can probably mock it for the converter
    function $(q) {
        if (q == "#textImportStartingLine")
            return {
                val: () => 1
            };
        else if (q == "#textImportMode")
            return {
                val: () => "newText"
            };
        else if (q == "#langSource")
            return {
                val: () => "la" // for now, maybe make flexible?
            };
    }

    epidoc_btn.addEventListener("click", () => {
        epidoc_target.value = "<ab>\n" + convertAncientText(epidoc_source.value, 'edr') + "\n</ab>"
    })
}