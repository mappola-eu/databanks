import json
from base64 import b64encode, b64decode
from subprocess import Popen, PIPE

if __name__ == "__main__":
    from epdioc_converter import *
else:
    from .epdioc_converter import *

def apply_replacements(str):
    str = str.replace('<a id="al1" />', '<a id="al1"></a>')
    str = str.replace("""class="textpart">
    <""", 'class="textpart"><')

    return str

def full_parse(epidoc):
    with generate_processor() as proc:
        diplomatic = apply_replacements(convert_to_diplomatic(proc, epidoc))
        interpretative = apply_replacements(convert_to_interpretative(proc, epidoc))
        metrics_visualised = apply_replacements((mv := convert_to_metrics_visualised(proc, epidoc)))
    
    return {
        'diplomatic': diplomatic,
        'interpretative': interpretative,
        'metrics_visualised': metrics_visualised
    }

def full_parse_on_inscription(inscription):
    epidoc = inscription.text_epidoc_form
    encoded = b64encode(epidoc.encode())

    pipe = Popen(['python3', __file__], stdin=PIPE, stdout=PIPE)
    response = pipe.communicate(encoded + b'\n', timeout=2)

    if not len(response[0]):
        inscription.text_interpretative_cached = "EPIDOC IS INVALID; UPDATE WITH WELL-FORMED XML"
        inscription.text_diplomatic_cached = "EPIDOC IS INVALID; UPDATE WITH WELL-FORMED XML"
        inscription.text_metrics_visualised_cached = "EPIDOC IS INVALID; UPDATE WITH WELL-FORMED XML"
        return inscription

    parsed = json.loads(response[0])

    inscription.text_interpretative_cached = parsed['interpretative']
    inscription.text_diplomatic_cached = parsed['diplomatic']
    inscription.text_metrics_visualised_cached = parsed['metrics_visualised']
    return inscription

if __name__ == '__main__':
    uinput = input()
    epidoc = b64decode(uinput.strip()).decode()
    parsed = full_parse(epidoc)
    print(json.dumps(parsed))