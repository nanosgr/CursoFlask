from my_app import app

app.config.from_object('configuration.DevelopmentConfig')
app.run()