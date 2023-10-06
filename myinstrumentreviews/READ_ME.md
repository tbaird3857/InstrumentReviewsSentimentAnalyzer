#Instrument Review App!

This app uses Flask as the web framework, with Python and HTML as the main languages. Users can input reviews of various musical instruments and submit them and view them. The data is stored in a SQLAlchemy table which can be viewed by users. Data analysis is performed by sentiment analysis, providing a way for users to see if their review is positive, negative, or neutral. All of the database instances can be viewed by users. Unit and integration tests are provided in the test_app.py file. 

#Forthcoming features:
CI/CD will be utilized with GitHub Actions.  RabbitMQ will be used to handle  event collaboration. The production environment will be with Docker. Production monitoring and instrumenting will be handled with Prometheus and Grafana.