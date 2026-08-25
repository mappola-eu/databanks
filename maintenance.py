import csv, json
import click
from flask import Blueprint
from .models import db, get_enum
from .linkage.epidoc import full_parse_on_inscription

maintenance = Blueprint('maintenance', __name__)

@maintenance.cli.command("rerender")
@click.argument("start_id", required=False)
def rerender(start_id=None):
    insc = get_enum('Inscriptions')
    iq = insc.query

    if start_id:
        iq = iq.filter(insc.id >= int(start_id))

    for i in iq.all():
        print("Starting", i.id)
        try:
            i = full_parse_on_inscription(i, timeout=10)
            if i.text_interpretative_cached == "EPIDOC IS INVALID; UPDATE WITH WELL-FORMED XML":
                print(f"\tInscription #{i.id} failed to render.")
            else:
                print("\tDone.")
        except e:
            print("\tFailed with error:", e)
    
    db.session.commit()
    print(f"Rerendered {insc.count()} inscriptions.")

@maintenance.cli.command("rebuild_inscription_search")
def rebuild_inscription_search():
    insc = get_enum('Inscriptions')

    for i in insc.query.all():
        i.make_searchable_inscription_cache()
    
    db.session.commit()
    #print("Done.")

@maintenance.cli.command("rebuild_ft")
def rebuild_ft():
    insc = get_enum('Inscriptions')

    for i in insc.query.all():
        i.make_fulltext_cache()
    
    db.session.commit()
    print("Done.")