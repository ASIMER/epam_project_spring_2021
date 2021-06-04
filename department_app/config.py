import os


class Config:
    """
    class container of environment variables
    """
    def __init__(self):
        self.SQLALCHEMY_DATABASE_URI = os.environ.get(
                "SQLALCHEMY_DATABASE_URI")
        self.SQLALCHEMY_TRACK_MODIFICATIONS = os.environ.get(
                "SQLALCHEMY_TRACK_MODIFICATIONS")
