from flask_frozen import Freezer

from dotenv import load_dotenv
load_dotenv()  # load environment before starting app

from app import create_app
app = create_app()

app.config['FREEZER_DESTINATION'] = "../docs"

freezer = Freezer(app)
freezer.freeze()
