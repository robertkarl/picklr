from blueprints import get_app

if __name__ == "__main__":
    app = get_app()
    app.run(host="0.0.0.0")
