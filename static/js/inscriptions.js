// Presentation switches
(() => {
    const presentation_switches = document.querySelectorAll('.insc--presentation-switches a');
    presentation_switches.forEach(presentation_switch => {
        presentation_switch.addEventListener('click', e => {
            const tgt = e.target;

            document.querySelector('.insc--text .insc--presentation.__active').classList.remove('__active');
            document.querySelector(tgt.getAttribute('href')).classList.add('__active');

            tgt.parentNode.querySelector('.__active').classList.remove('__active');
            tgt.classList.add('__active');

            e.preventDefault();
        })
    });
})();

// Insc cards
(() => {
    const insc_cards = document.querySelectorAll('.insc--card .insc--card-header');
    insc_cards.forEach(card => {
        card.addEventListener('click', e => {
            const tgt = e.target;

            tgt.parentNode.classList.toggle('__active');
            tgt.classList.toggle('__active');

            e.preventDefault();
        })
    });
})();