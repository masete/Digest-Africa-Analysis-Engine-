from . import bp
from flask import render_template
from flask_login import login_required
from dashapp import dash_companies, dash_investors, dash_companiesDetails, dash_deals1,\
    dash_invstormap, dash_investorDetails, dash_deals2


# @bp.route("/companies")
# @login_required
# def companies_template():
#     return render_template("companies.html", dash_url=dash_companies.url_base)


@bp.route("/companiesDetails")
@login_required
def companies_details_template():
    return render_template("companiesDetails.html", dash_url=dash_companiesDetails.url_base)


@bp.route("/investors")
@login_required
def investors_template():
    return render_template("investors.html", dash_url=dash_investors.url_base)


@bp.route("/investormap")
@login_required
def investor_map():
    return render_template("investormap.html", dash_url=dash_invstormap.url_base)


@bp.route("/investorDetails")
@login_required
def investorDetails():
    return render_template("investorDetails.html", dash_url=dash_investorDetails.url_base)


@bp.route("/deals1")
@login_required
def deals1_template():
    return render_template("deals1.html", dash_url=dash_deals1.url_base)


@bp.route("/deals2")
@login_required
def deals2_template():
    return render_template("deals2.html", dash_url=dash_deals2.url_base)

