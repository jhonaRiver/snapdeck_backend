#!/usr/bin/env python3

from app import create_app
from app.models import db


def create_database():
    app = create_app()
    with app.app_context():
        db.create_all()


if __name__ == '__main__':
    create_database()
