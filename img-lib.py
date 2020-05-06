#!/usr/bin/env python3
# Import modules for CGI handling
# Ресайз, конвертер, вставка логотипа, водяные знаки
#
# apt install python3-pymysql
#
# example: GET /cgi-bin/test.py?query=list_all_images
#

import cgi
import cgitb
import pymysql
import json
import os

from pathlib import Path
from pymysql.cursors import DictCursor


def list_all_images():
    count_files = 0
    files = {}
    request = {}

    directory = Path(os.getcwd()).parent
    extension = ".jpg,.jpeg,.png"
    extensions = extension.split(',')

    for image in directory.glob('**/*'):
        if image.is_file() and all(not str(image).lower().endswith(ext) for ext in extensions):
            continue

        if image.is_dir():
            continue

        files[count_files] = str(image)
        count_files = count_files + 1

    request['directory'] = str(directory)
    request['files'] = files

    return(files)


if __name__ == '__main__':  # Required arguments
    con = pymysql.connect(
        'localhost', 'admin_console', 'xxxx', 'admin_console')

    xauthtoken = "45647"
    with con: # Проверка авторизации
        cur = con.cursor()
        cur.execute(
            "SELECT user_login_id, user_id FROM md_users_login WHERE xauthtoken=%s", xauthtoken)
        row = cur.fetchone()

    # Create instance of FieldStorage 
    form = cgi.FieldStorage()
    # Get data from fields
    query = form.getvalue('query')


    print("Content-type:application/json\n\n")

    data = {}
    if row == None:
        data['db_message'] = "Не авторизованный сеанс"
    else:
        data['db_message'] = row


    if query == "list_all_images":
        data['request'] = list_all_images()


    print(json.dumps(data))
