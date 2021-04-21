from dash import Dash
from .dash_func import apply_layout_with_auth, _protect_dashviews
from dashapp.dataTables.callbacks.callbacks import register_callbacks
from dashapp.dataTables.layouts.dtlayout import layout
import dash_bootstrap_components as dbc


url_base = "/dash/dashTables/"


def add_dash(server):
    meta_viewport = {
        "name": "viewport",
        "content": "width=device-width, initial-scale=1, shrink-to-fit=no",
    }

    external_css = ["https://cdnjs.cloudflare.com/ajax/libs/normalize/7.0.0/normalize.min.css",
                    "https://cdnjs.cloudflare.com/ajax/libs/skeleton/2.0.4/skeleton.min.css",
                    "//fonts.googleapis.com/css?family=Raleway:400,300,600",
                    "https://codepen.io/bcd/pen/KQrXdb.css",
                    "https://maxcdn.bootstrapcdn.com/font-awesome/4.7.0/css/font-awesome.min.css",
                    "https://codepen.io/dmcomfort/pen/JzdzEZ.css"]



    external_js = ["https://code.jquery.com/jquery-3.2.1.min.js",
                   "https://codepen.io/bcd/pen/YaXojL.js"]
    external_stylesheets = [dbc.themes.LUX]
    # external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]
    app = Dash(
        server=server,
        url_base_pathname=url_base,
        meta_tags=[meta_viewport],
        external_stylesheets=external_stylesheets,

    )
    for css in external_css:
        app.css.append_css({"external_url": css})
    for js in external_js:
        app.scripts.append_script({"external_url": js})
    app.url_base_pathname = url_base
    apply_layout_with_auth(app, layout(app))
    register_callbacks(app)
    _protect_dashviews(app)

    return app.server
