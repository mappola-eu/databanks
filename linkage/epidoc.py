from xml.dom.minidom import parseString

def epidoc_to_diplomatic(epidoc):
    text = ""

    xml = "<epidoc>" + epidoc + "</epidoc>"
    md = parseString(xml)
    root = md.childNodes[0]

    print(root.childNodes[1].nodeName)

    for child in root.childNodes:
        if child.nodeName == "#text":
            text += child.nodeValue.strip("\n").upper()
        elif child.nodeName == "lb":
            if len(text) != 0:
                text += "\n"
        elif child.nodeName == "expan":
            for expan_child in child.childNodes:
                if expan_child.nodeName == "#text":
                    text += expan_child.nodeValue.strip("\n").upper()
                elif expan_child.nodeName != "ex":
                    text += expan_child.childNodes[0].nodeValue.strip("\n").upper()
        elif child.nodeName == "supplied":
            length = len(child.childNodes[0].nodeValue.strip("\n"))
            text += " " * length
        else:
            print(child.nodeName)

    return text