from . import bp
from flask import render_template
from flask_login import login_required
from dashapp import dash_companies, dash_investors, dash_companiesDetails, dash_deals1


@bp.route("/companies")
@login_required
def companies_template():
    return render_template("companies.html", dash_url=dash_companies.url_base)


@bp.route("/companiesDetails")
@login_required
def companies_details_template():
    return render_template("companiesDetails.html", dash_url=dash_companiesDetails.url_base)


@bp.route("/investors")
@login_required
def investors_template():
    return render_template("investors.html", dash_url=dash_investors.url_base)


@bp.route("/deals")
@login_required
def deals1_template():
    return render_template("investors.html", dash_url=dash_deals1.url_base)


# @bp.route("/deals")
# @login_required
# def deals2_template():
#     return render_template("investors.html", dash_url=dash_deals2.url_base)
#