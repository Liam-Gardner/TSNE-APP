import os


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    DATA_UPLOAD_FOLDER = "uploads/data"
    PLOTS_UPLOAD_FOLDER = "app/static"
    TEMPLATES_FOLDER = "app/templates"

