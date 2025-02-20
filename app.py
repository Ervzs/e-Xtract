from blueprints import create_app

app = create_app() #passes configurations to app variable

# create_app() is defined inside blueprints/__init__.py

if __name__ == "__main__":
    app.run()