import xml.etree.ElementTree as ET
from saxonpy import PySaxonProcessor

def generate_processor():
    return PySaxonProcessor(license=False)

def _apply_stylesheet(proc, xml_intro, props=None):
    if props is None:
        props = {}

    xsltproc = proc.new_xslt_processor()
    
    document = proc.parse_xml(xml_text=xml_intro)

    xsltproc.set_source(xdm_node=document)
    xsltproc.compile_stylesheet(stylesheet_file="./epidoc_styles/start-edition.xsl")

    for k, v in props.items():
        xsltproc.set_parameter(k, proc.make_string_value(v))

    transformed_xml = xsltproc.transform_to_string()
    
    tree = ET.fromstring(transformed_xml)
    output_element = tree.find(".//*[@id=\"edition\"]/*")
    ET.indent(output_element, space='    ')
    output = ET.tostring(output_element).decode()

    return output

def _prepare(xml_intro):
    return '<?xml version="1.0" encoding="UTF-8"?><?xml-model href="http://www.stoa.org/epidoc/schema/latest/tei-epidoc.rng" schematypens="http://relaxng.org/ns/structure/1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div type="edition" xml:space="preserve">' + xml_intro + '</div></body></text></TEI>'

def convert_to_diplomatic(proc, xml_intro):
    return _apply_stylesheet(proc, _prepare(xml_intro), { "edition-type": "diplomatic",
                                                          "leiden-style": "edh-web",
                                                          "internal-app-style": "none"
                                                        })

def convert_to_interpretative(proc, xml_intro):
    return _apply_stylesheet(proc, _prepare(xml_intro), { "edition-type": "interpretive",
                                                          "leiden-style": "edh-web",
                                                          "internal-app-style": "none"
                                                        })

def convert_to_metrics_visualised(proc, xml_intro):
    return _apply_stylesheet(proc, _prepare(xml_intro), { "edition-type": "interpretive",
                                                          "verse-lines": "on",
                                                          "internal-app-style": "none"
                                                        })