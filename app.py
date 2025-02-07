from blueprints import create_app

app = create_app() #passes configurations to app variable

if __name__ == "__main__":
    app.run()