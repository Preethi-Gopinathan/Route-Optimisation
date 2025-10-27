from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 Hello from Flask on Elastic Beanstalk deployed using GitHub Actions + CDK!"
