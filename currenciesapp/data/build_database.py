import os

from currenciesapp import db, create_app

if __name__ == '__main__':
    app = create_app()
    with app.app_context():
        f = open(os.path.abspath("../../db_scripts/BUILD_DATABASE.sql"), 'r', encoding='utf-8')
        query = " ".join(f.readlines())
        db.engine.execute(query)
        f.close()
        f = open(os.path.abspath("../../db_scripts/CONSTANT_DATA.sql"), 'r', encoding='utf-8')
        query = " ".join(f.readlines())
        print(query)
        db.engine.execute(query)
        f.close()
