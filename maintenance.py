import csv, json
import click
from flask import Blueprint
from .models import db, get_enum
from .linkage.epidoc import full_parse_on_inscription

maintenance = Blueprint('maintenance', __name__)

@maintenance.cli.command("rerender")
def rerender():
    insc = get_enum('Inscriptions')

    for i in insc.query.all():
        i = full_parse_on_inscription(i)
        if i.text_interpretative_cached == "EPIDOC IS INVALID; UPDATE WITH WELL-FORMED XML":
            print(f"Inscription #{i.id} failed to render.")
    
    db.session.commit()
    print("Done.")