from my_app import app
import os
from dotenv import load_dotenv
load_dotenv()  # take environment variables from .env.

if os.getenv('DEBUG_STATE') == 'True':
    app.run(port=os.getenv('PORT'), debug=True)
elif os.getenv('DEBUG_STATE') == 'False':
    app.run(port=os.getenv('PORT'), debug=False)
