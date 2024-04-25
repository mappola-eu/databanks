document.querySelectorAll("[data-epidoc-bar]").forEach((item) => {
    new Bar(item, 
    [
        {
            "type": "counter",
            "options": [
                {
                    "label": "(lb)", "description": "New line marker",
                    "modify": (before, inner, after, n) => {
                        return before + inner + '<lb n="' + n + '"/>' + after
                    }
                },
                {
                    "label": "in word", "description": "New line (in word) marker",
                    "modify": (before, inner, after, n) => {
                        return before + inner + '<lb n="' + n + '" break="no"/>' + after
                    }
                },
            ]
        },
        {
            "type": "choice", "label": "(lg)", "description": "",
            "options": {
                "dactylic.hexameter": "Hexameter",
                "elegiac.couplet": "Elegiac couplet",
                "dactylic.rhythm": "Dactylic Rhythm",
                "iambic.trimeter": "Iambic Trimeter",
                "iambic.rhythm": "Iambic Rhythm"
            },
            "modify": (before, inner, after, c) => {
                return before + '<lg met="' + c +'">' + inner + '</lg>' + after
            }
        },
        {
            "type": "choice", "label": "(l)", "description": "",
            "options": {
                "dactylic.hexameter": "Hexameter",
                "elegiac.couplet": "Elegiac couplet",
                "dactylic.rhythm": "Dactylic Rhythm",
                "iambic.trimeter": "Iambic Trimeter",
                "iambic.rhythm": "Iambic Rhythm"
            },
            "modify": (before, inner, after, c) => {
                return before + '<l met="' + c +'">' + inner + '</l>' + after
            }
        },
        {
            "type": "insert", "label": "ạ", "description": "Unclear letter(s)",
            "modify": (before, inner, after) => {
                return before + '<unclear>' + inner + '</unclear>' + after
            }
        },
        {
            "type": "insert", "label": "á", "description": "Letter with apex",
            "modify": (before, inner, after) => {
                return before + '<hi rend="apex">' + inner + '</hi>' + after
            }
        },
        {
            "type": "insert", "label": "ā", "description": "Letter with supraline",
            "modify": (before, inner, after) => {
                return before + '<hi rend="supraline">' + inner + '</hi>' + after
            }
        },
        {
            "type": "insert", "label": "a͡b", "description": "Letters with ligature",
            "modify": (before, inner, after) => {
                return before + '<hi rend="ligature">' + inner + '</hi>' + after
            }
        },
        {
            "type": "insert", "label": "[a]", "description": "Restauration",
            "modify": (before, inner, after) => {
                return before + '<supplied reason="lost">' + inner + '</supplied>' + after
            }
        },
        {
            "type": "insert", "label": "[a?]", "description": "Uncertain restauration",
            "modify": (before, inner, after) => {
                return before + '<supplied reason="lost" cert="low">' + inner + '</supplied>' + after
            }
        },
        {
            "type": "insert", "label": "{a}", "description": "Surplus",
            "modify": (before, inner, after) => {
                return before + '<surplus>' + inner + '</surplus>' + after
            }
        },
        {
            "type": "insert", "label": "⸢a⸣", "description": "Correction",
            "modify": (before, inner, after) => {
                return before + '<choice><corr>' + inner + '</corr><sic></sic></choice>' + after
            }
        },
        {
            "type": "insert", "label": "(!)", "description": "Regularisation",
            "modify": (before, inner, after) => {
                return before + '<choice><reg>' + inner + '</reg><orig></orig></choice>' + after
            }
        },
        {
            "type": "insert", "label": "<a>", "description": "Letters added by editor",
            "modify": (before, inner, after) => {
                return before + '<supplied reason="omitted">' + inner + '</supplied>' + after
            }
        },
        {
            "type": "insert", "label": "⟦a⟧", "description": "Erasure",
            "modify": (before, inner, after) => {
                return before + '<del rend="erasure">' + inner + '</del>' + after
            }
        },
        {
            "type": "choice", "label": "a(b)c(d)", "description": "Complex abbreviation",
            "options": {
                "co-n-s-ul": "co(n)s(ul)",
                "proco-n-s-ul": "proco(n)s(ul)",
                "c-o-ho-rs": "c(o)ho(rs)",
                "---": "()()",
            },
            "modify": (before, inner, after, c) => {
                let cc = c.split("-")
                return before + inner + '<expan><abbr>' + cc[0] + '</abbr><ex>' + cc[1] + '</ex><abbr>' +
                        cc[2] + '</abbr><ex>' + cc[3] + '</ex></expan>' + after
            }
        },
        {
            "type": "insert", "label": "a(bc?)", "description": "Tentative expansion of an abbreviation",
            "modify": (before, inner, after) => {
                return before + '<expan><abbr>' + inner + '</abbr><ex cert="low"></ex></expan>' + after
            }
        },
        {
            "type": "insert", "label": "a(---)", "description": "Abbreviation with unknown development",
            "modify": (before, inner, after) => {
                return before + '<abbr>' + inner + '</abbr>' + after
            }
        },
        {
            "type": "insert", "label": "(abc)", "description": "Expansion of a symbol",
            "modify": (before, inner, after) => {
                return before + '<expan><ex>' + inner + '</ex></expan>' + after
            }
        },
        {
            "type": "choice", "label": "Lacuna", "description": "",
            "options": {
                "let_unknown": "Letters - Extent unknown [- - -]",
                "let_approx": "Letters - Approximate extent [- ca. 5 -]",
                "let_range": "Letters - Range of possible extent [- 5-7 -]",
                "let1": "Letters - 1 letter",
                "let2": "Letters - 2 letters",
                "let3": "Letters - 3 letters",
                "let4": "Letters - 4 letters",
                "let5": "Letters - 5 letters",
                "line_unknown": "Lines - Number unknown",
                "line1": "Lines - 1 line",
            },
            "modify": (before, inner, after, c) => {
                let choices = {
                    "let_unknown": '<gap reason="lost" extent="unknown" unit="character"/>',
                    "let_approx": '<gap reason="lost" quantity="5" unit="character" precision="low"/>',
                    "let_range": '<gap reason="lost" atLeast="5" atMost="7" unit="character"/>',
                    "let1": '<gap reason="lost" quantity="1" unit="character"/>',
                    "let2": '<gap reason="lost" quantity="2" unit="character"/>',
                    "let3": '<gap reason="lost" quantity="3" unit="character"/>',
                    "let4": '<gap reason="lost" quantity="4" unit="character"/>',
                    "let5": '<gap reason="lost" quantity="5" unit="character"/>',
                    "line_unknown": '<gap reason="lost" extent="unknown" unit="line"/>',
                    "line1": '<gap reason="lost" quantity="1" unit="line"/>'
                }
                return before + inner + choices[c] + after
            }
        },
        {
            "type": "choice", "label": "Addition", "description": "",
            "options": {
                "above": "Above",
                "below": "Below"
            },
            "modify": (before, inner, after, c) => {
                return before + '<add place="' + c + '">' + inner + '</add>' + after
            }
        },
        {
            "type": "choice", "label": "Illegible", "description": "",
            "options": {
                "let1": "Letters - 1 letter",
                "let2": "Letters - 2 letters",
                "let3": "Letters - 3 letters",
                "let4": "Letters - 4 letters",
                "let5": "Letters - 5 letters"
            },
            "modify": (before, inner, after, c) => {
                let choices = {
                    "let1": '<gap reason="illegible" quantity="1" unit="character"/>',
                    "let2": '<gap reason="illegible" quantity="2" unit="character"/>',
                    "let3": '<gap reason="illegible" quantity="3" unit="character"/>',
                    "let4": '<gap reason="illegible" quantity="4" unit="character"/>',
                    "let5": '<gap reason="illegible" quantity="5" unit="character"/>',
                }
                return before + inner + choices[c] + after
            }
        },
        {
            "type": "insert", "label": "Vacat", "description": "Undetermined vacat",
            "modify": (before, inner, after) => {
                return before + inner + '<space extent="unknown" unit="character"/>' + after
            }
        },
        {
            "type": "choice", "label": "Symbol", "description": "",
            "options": {
                "hedera": "hedera",
                "crux": "crux",
                "monogramma Christi": "monogramma Christi",
                "ancora": "ancora",
                "siglum": "siglum",
            },
            "modify": (before, inner, after, c) => {
                return before + inner + '<g type="' + c + '"/>' + after
            }
        }
    ],
    (input) => {
        let full_xml = '<?xml version="1.0" encoding="UTF-8"?><?xml-model href="http://www.stoa.org/epidoc/schema/latest/tei-epidoc.rng" schematypens="http://relaxng.org/ns/structure/1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div type="edition" xml:space="preserve">' + input + '</div></body></text></TEI>'
        
        let domParser = new DOMParser();
        let dom = domParser.parseFromString(full_xml, 'text/xml')

        if (dom.documentElement.nodeName == 'parsererror') {
            let errors = []
            let errorNodes = dom.querySelectorAll("parsererror")

            errorNodes.forEach((errorNode) => {
                let msg = errorNode.innerHTML.split("\n")[0]
                msg = msg.replace(/\&lt;/g, '<')
                msg = msg.replace(/\&gt;/g, '>')
                errors.push(msg)
            })

            return {
                success: false,
                messages: errors
            }
        } else {
            return {
                success: true,
                messages: []
            }
        }
    },
    {
        validation: {
            ok: "Everything looks fine!",
            bad: "Oops. There are some errors in your XML:"
        }
    })
})