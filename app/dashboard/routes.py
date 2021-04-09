from . import bp
from flask import render_template
from flask_login import login_required
from dashapp import dash_investors, dash_companiesDetails, dash_deals1


@bp.route("/companiesDetails")
@login_required
def companies_details_template():
    return render_template("companiesDetails.html", dash_url=dash_companiesDetails.url_base)


@bp.route("/investors")
@login_required
def investors_template():
    return render_template("investors.html", dash_url=dash_investors.url_base)


@bp.route("/deals1")
@login_required
def deals1_template():
    return render_template("deals1.html", dash_url=dash_deals1.url_base)


@bp.route("/companies_data")
@login_required
def companies_data_template():
    return render_template("companies_data.html")
