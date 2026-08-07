from flask import Blueprint, render_template, make_response, abort, send_file, request, flash, Response
from ..models import Inscriptions, WorkStatus, inscriptions_to_json, inscriptions_to_csv
from flask_security import login_required

import csv, io, random, zipfile

inscriptions = Blueprint('inscriptions', __name__)


@inscriptions.route("/map")
def map():
    inscs = Inscriptions.query.all()
    inscs = [*filter(lambda i: not i.work_status or not i.work_status.is_deleted, inscs)]

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


@inscriptions.route("/download-xml", methods=["GET", "POST"])
def download_xml():
    if request.method == 'POST':
        captcha = Inscriptions.query.get_or_404(request.form['cid'])

        if captcha.title.strip() == request.form['ctitle'].strip():
            zip_file = _generate_zipfile()

            return Response(zip_file, mimetype='application/zip', headers={
                'Content-Disposition': f'attachment;filename=MAPPOLADATA.zip'
            })


        else:
            flash("Error: The captcha input was invalid.")

    acceptable_work_status = WorkStatus.query.filter_by(is_complete=True).first()
    captcha_insc_query = Inscriptions.query.filter_by(work_status=acceptable_work_status)
    max_offset = captcha_insc_query.count()
    captcha_insc = captcha_insc_query.offset(random.randint(0, max_offset - 1)).first()

    return render_template("inscriptions/download_xml.html", captcha_insc=captcha_insc)


@login_required
@inscriptions.route("/.unknown/alex.csv")
def alex_export():
    inscs = Inscriptions.query.all()
    inscs = [*filter(lambda i: not i.work_status or not i.work_status.is_deleted, inscs)]

    csvdata = inscriptions_to_csv(inscs)

    csv_io = io.StringIO()
    csvwriter = csv.writer(csv_io, delimiter=',', quotechar='\"')
    csvwriter.writerows(csvdata)

    mem_io = io.BytesIO()
    mem_io.write(csv_io.getvalue().encode())
    mem_io.seek(0)

    return send_file(mem_io, mimetype='text/csv')


def _generate_zipfile():
    zip_io = io.BytesIO()
    zip_file = zipfile.ZipFile(zip_io, mode='w')

    for insc in Inscriptions.query.all():
        if insc.work_status and insc.work_status.is_deleted:
            continue

        xml_file = render_template("inscriptions/one.xml", insc=insc)
        zip_file.writestr(f"{insc.long_id()}.xml", xml_file)
    
    zip_file.close()

    return zip_io.getvalue()