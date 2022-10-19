from flask_migrate import Migrate
from app import create_app, db
from app.models import Users, Entreprenuers, Transactions, Investors


app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {"db": db, "User": Users,
            "Entreprenuers": Entreprenuers, "Transactions": Transactions, "Investors": Investors}


if __name__ == "__main__":
    app.run(debug=False)

