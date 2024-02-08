import xml.etree.ElementTree as ET
import re
from saxonpy import PySaxonProcessor

def generate_processor():
    return PySaxonProcessor(license=False)

def _apply_stylesheet(proc, xml_intro, props=None):
    if props is None:
        props = {}

    if 'verse-lines' in props and props['verse-lines'] == 'on':
        # ignore all <lb />s
        xml_intro = re.subn("\<lb( n=\"[0-9]*\")?/>", '', xml_intro)[0]
        xml_intro = re.subn("(\r?\n)*\<lb( n=\"[0-9]*\")? break=\"no\"/>", '', xml_intro)[0]

    xsltproc = proc.new_xslt_processor()
    
    document = proc.parse_xml(xml_text=xml_intro)

    xsltproc.set_source(xdm_node=document)
    xsltproc.compile_stylesheet(stylesheet_file="./epidoc_styles/start-edition.xsl")

    for k, v in props.items():
        xsltproc.set_parameter(k, proc.make_string_value(v))

    transformed_xml = xsltproc.transform_to_string()
    
    tree = ET.fromstring(transformed_xml)
    output_element = tree.find(".//*[@id=\"edition\"]/*[@class='textpart']")
    output = ET.tostring(output_element, short_empty_elements=False).decode()
    output = output.replace("></br>", "/>")

    if props['internal-app-style'] != 'none':
        app_output_element = tree.find(".//*[@id=\"apparatus\"]")

        if app_output_element is None:
            app_output_element = tree.find(".//*[@class=\"miniapp\"]")

        if app_output_element is not None:
            app_output = ET.tostring(app_output_element, short_empty_elements=False).decode()
            app_output = app_output.replace("></br>", "/>")
            app_output = app_output.replace(" | l.", "<br/>l.")

            output = output + '~~~APP BELOW~~~' + app_output

    return output

def _prepare(xml_intro):
    return '<?xml version="1.0" encoding="UTF-8"?><?xml-model href="http://www.stoa.org/epidoc/schema/latest/tei-epidoc.rng" schematypens="http://relaxng.org/ns/structure/1.0"?><TEI xmlns="http://www.tei-c.org/ns/1.0"><text><body><div type="edition" xml:space="preserve">' + xml_intro + '</div></body></text></TEI>'

def convert_to_diplomatic(proc, xml_intro):
    return _apply_stylesheet(proc, _prepare(xml_intro), { "edition-type": "diplomatic",
                                                          "leiden-style": "panciera",
                                                          "internal-app-style": "none"
                                                        })

def convert_to_interpretative(proc, xml_intro):
    return _apply_stylesheet(proc, _prepare(xml_intro), { "edition-type": "interpretive",
                                                          "leiden-style": "panciera",
                                                          "internal-app-style": "minex"
                                                        })

def convert_to_metrics_visualised(proc, xml_intro):
    return _apply_stylesheet(proc, _prepare(xml_intro), { "edition-type": "interpretive",
                                                          "leiden-style": "panciera",
                                                          "verse-lines": "on",
                                                          "internal-app-style": "none"
                                                        })