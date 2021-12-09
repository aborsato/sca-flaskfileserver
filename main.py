# ░▄▀▀░▄▀▀▒▄▀▄
# ░▀▄▄▒▄██░█▀█
# Microsoft

"""
This app serves static files from a specific location and checks
if the given user (from Request Header or Cookie) is the owner
or the file uploaded date is older than one year.
"""

import os
from datetime import datetime

from dateutil.relativedelta import relativedelta
from flask import Flask, abort, request, send_file
from sqlalchemy import and_, create_engine, or_, select
from sqlalchemy.orm import Session
from sqlalchemy.pool import SingletonThreadPool

from database import Base, Metadata

# TODO: change this variable to point to the root folder of your download path
ROOT_DOWNLOAD_PATH = '.'
app = Flask(__name__)

# maintain the same connection across all threads
# TODO: change the engine to point to your database
engine = create_engine('sqlite:///database.sqlite3', poolclass=SingletonThreadPool, echo=True)
Base.metadata.create_all(engine)
session = Session(engine, future=True)


@app.route('/download/<file_name>')
def download_file(file_name=None):
    # check user credentials (accepts request parameter or header)
    user_name = request.args.get('user', request.headers.get('user', request.cookies.get('user', '')))

    # check if the user have access to the requested file and the file exists
    # TODO: change the query to filter by your own criteria
    one_year_back = datetime.today() + relativedelta(years=-1)
    query_file = select(Metadata).where(
        and_(
            Metadata.file_name == file_name,
            or_(
                Metadata.owner == user_name, # the user is the owner of the file
                Metadata.uploaded_date <= one_year_back # the file is older than 1 year
            )
        )
    )

    # download the file if the record exists in the database
    if session.execute(query_file).all():
        file_path = os.path.join(ROOT_DOWNLOAD_PATH, file_name)
        return send_file(file_path, as_attachment=True)

    # abort the request with 404 (NOT FOUND) otherwise
    abort(404)

if __name__ == "__main__":
    app.run()
