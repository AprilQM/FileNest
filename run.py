from app import create_app
from config import Config

app = create_app()

if __name__ == '__main__':
    app.run(debug=Config.WEBCONFIG["rear"]['debug'], port=Config.WEBCONFIG["rear"]['port'], host=Config.WEBCONFIG["rear"]['host'])
