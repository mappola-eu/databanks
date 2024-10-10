from flask import Blueprint, render_template, make_response, abort, send_file
from ..models import Inscriptions, inscriptions_to_json, inscriptions_to_csv
from flask_security import login_required

import csv, io

inscriptions = Blueprint('inscriptions', __name__)


@inscriptions.route("/map")
def map():
    inscs = Inscriptions.query.all()

    mc = inscriptions_to_json(inscs)

    return render_template("inscriptions/map.html", mc=mc)


@inscriptions.route("/MPL<id>.xml")
def render_xml(id):
    insc = Inscriptions.query.filter_by(id=int(id)).one_or_none()

    if not insc:
        abort(404)

    xml_file = render_template("inscriptions/one.xml", insc=insc)
    response = make_response(xml_file)
    response.headers['Content-Type'] = 'application/xml'

    return response


@login_required
@inscriptions.route("/.unknown/alex.csv")
def alex_export():
    inscs = Inscriptions.query.all()

    csvdata = inscriptions_to_csv(inscs)

    csv_io = io.StringIO()
    csvwriter = csv.writer(csv_io, delimiter=',', quotechar='\"')
    csvwriter.writerows(csvdata)

    mem_io = io.BytesIO()
    mem_io.write(csv_io.getvalue().encode())
    mem_io.seek(0)

    return send_file(mem_io, mimetype='text/csv')