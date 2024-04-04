class Bar {
    constructor(target, header, verifier, language) {
        this.target = target
        this.header = header
        this.verifier = verifier
        this.language = language

        this.parseDOM()
        this.makeDOM()
        this.validate()
    }

    parseDOM() {
        this.input = this.target.querySelector('textarea')
        this.input.addEventListener("change", this.validate.bind(this))
    }

    makeDOM() {
        let button_row = this.makeButtonRow()
        for (let item of this.header) {
            this.makeHeaderItem(button_row, item)
        }
        this.makeValidatorRow()
    }

    validate() {
        let result = this.verifier(this.input.value)
        this.updateValidatorRow(result)
    }

    makeButtonRow() {
        let button_row = document.createElement('div')
        button_row.classList.add('bar-button-row')
        this.target.insertBefore(button_row, this.input)
        return button_row
    }

    makeHeaderItem(button_row, item) {
        switch (item.type) {
            case 'insert':
                this.makeInsertItem(button_row, item)
                break;
            case 'counter':
                this.makeCounterItem(button_row, item)
                break;
            case 'choice':
                this.makeChoiceItem(button_row, item)
                break;
        }
    }

    makeInsertItem(button_row, item) {
        let insert_item = document.createElement('button')
        insert_item.classList.add('bar-button')
        insert_item.title = item.description
        insert_item.type = 'button'
        insert_item.innerText = item.label
        button_row.appendChild(insert_item)

        insert_item.addEventListener('click', (() => {
            this.doInsert(item)
            this.input.focus()
        }).bind(this))
    }

    makeCounterItem(button_row, item) {
        let counter_item = document.createElement('div')
        counter_item.classList.add('bar-counter')
        button_row.appendChild(counter_item)

        let counter_item_input = document.createElement('input')
        counter_item_input.classList.add('bar-counter-input')
        counter_item_input.type = 'number'
        counter_item_input.value = 1
        counter_item_input.min = 1
        counter_item.appendChild(counter_item_input)

        for (const option of item.options) {
            let counter_item_btn = document.createElement('button')
            counter_item_btn.classList.add('bar-counter-button')
            counter_item_btn.title = option.description
            counter_item_btn.type = 'button'
            counter_item_btn.innerText = option.label
            counter_item.appendChild(counter_item_btn)

            counter_item_btn.addEventListener('click', (() => {
                this.doCounter(option, counter_item_input)
                this.input.focus()
            }).bind(this))   
        }
    }

    makeChoiceItem(button_row, item) {
        let choice_item = document.createElement('div')
        choice_item.classList.add('bar-choice')
        button_row.appendChild(choice_item)

        let choice_item_select = document.createElement('select')
        choice_item_select.classList.add('bar-choice-select')
        choice_item.appendChild(choice_item_select)

        for (const option of Object.keys(item.options)) {
            let choice_item_select_option = document.createElement('option')
            choice_item_select_option.value = option
            choice_item_select_option.innerText = item.options[option]
            choice_item_select.appendChild(choice_item_select_option)
        }

        let choice_item_btn = document.createElement('button')
        choice_item_btn.classList.add('bar-choice-button')
        choice_item_btn.title = item.description
        choice_item_btn.type = 'button'
        choice_item_btn.innerText = item.label
        choice_item.appendChild(choice_item_btn)

        choice_item_btn.addEventListener('click', (() => {
            this.doChoice(item, choice_item_select)
            this.input.focus()
        }).bind(this))
    }

    makeValidatorRow() {
        this.validator_row = document.createElement('div')
        this.validator_row.classList.add('bar-validator')
        this.target.appendChild(this.validator_row)
    }

    updateValidatorRow(result) {
        this.validator_row.innerHTML = ""

        if (result.success) {
            this.makePositiveResult()
        } else {
            this.makeNegativeResult(result)
        }
    }

    makePositiveResult() {
        let validation = document.createElement('div')
        validation.classList.add('bar-validator-result', 'result-is-positive')
        validation.innerText = this.language.validation.ok;
        this.validator_row.appendChild(validation)
    }

    makeNegativeResult(result) {
        let validation = document.createElement('div')
        validation.classList.add('bar-validator-result', 'result-is-negative')
        validation.innerText = this.language.validation.bad;
        this.validator_row.appendChild(validation)

        result.messages.forEach((msg) => {
            let validation = document.createElement('div')
            validation.classList.add('bar-validator-msg', 'result-is-negative')
            validation.innerText = msg;
            this.validator_row.appendChild(validation)
        })
    }

    doInsert(item) {
        this._getSelection()
        this.input.value = item.modify(this.__before, this.__inner, this.__after)
        this._setSelection()
        this.validate()
    }

    doCounter(item, counter) {
        this._getSelection()
        this.input.value = item.modify(this.__before, this.__inner, this.__after, counter.value)
        counter.value = parseInt(counter.value) + 1
        this._setSelection()
        this.validate()
    }

    doChoice(item, choice) {
        this._getSelection()
        this.input.value = item.modify(this.__before, this.__inner, this.__after, choice.value)
        this._setSelection()
        this.validate()
    }

    _getSelection() {
        this.__before = this.input.value.substring(0, this.input.selectionStart)
        this.__inner = this.input.value.substring(this.input.selectionStart, this.input.selectionEnd)
        this.__after = this.input.value.substring(this.input.selectionEnd)

        this.__from_end = this.input.value.length - this.input.selectionEnd;
    }

    _setSelection() {
        this.input.selectionStart = this.__before.length
        this.input.selectionEnd = this.input.value.length - this.__from_end
    }
}