from faker import Faker


def select_or_create_db(couchserver, db_name):
    if db_name in couchserver:
        db = couchserver[db_name]
        print("already exist")
    else:
        db = couchserver.create(db_name)
        print("creating")
    return db


def generate_random_data(n_rows):
    data = []
    fake = Faker('it_IT')

    for _ in range(n_rows):
        doc = {'name': (fake.name())}
        data.append(doc)
    return data


def populate_db(db, data):
    print(f"populate {db} with {len(data)} rows")
    return db.update(data)
