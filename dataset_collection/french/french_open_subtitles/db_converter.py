import sqlite3
import os
import argparse
# zip
import zipfile
import shutil


def save(name, file, path):
    # name = name.split('"')[1]
    with open('{}/{}.zip'.format(path, name), 'wb') as w:
        w.write(file)

    with zipfile.ZipFile('{}/{}.zip'.format(path, name), 'r') as zip_ref:
        zip_ref.extractall('{}/{}'.format(path, name))

    # remove file
    os.remove('{}/{}.zip'.format(path, name))


def get_range():
    with con:
        cur = con.cursor()
        cur.execute("select * from zipfiles")
        rows = cur.fetchall()
    print(rows)
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--path', help='path', required=False)
    parser.add_argument('-d', '--db', help='db', required=False)
    args = vars(parser.parse_args())

    con = sqlite3.connect(args.get('db'))
    con.row_factory = sqlite3.Row
    path = args.get('path')

    if not os.path.isdir(path):
        os.mkdir(path)

    rows = get_range()
    for row in rows:
        print(row)
        save(row['name'], row['content'], path)
