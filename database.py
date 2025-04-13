import json

# if you have a UnicodeDecodeError try anuther encoding format:
# for english and other:
# utf-8, utf-16, latin-1
# for russian and other:
# cyrillic
encodingFormat = "utf-8"

def json_create(key, value, database_name):
    convert = {key: value}

    with open(f"{database_name}.json", "w", encoding=encodingFormat) as db:
        json.dump(convert, db)

def json_change(key, value, database_name):
    with open(f"{database_name}.json", "r", encoding=encodingFormat) as db:
        convert = json.load(db)

    convert[key] = value

    with open(f"{database_name}.json", "w", encoding=encodingFormat) as db:
        json.dump(convert, db)

def json_read(key, database_name):
    with open(f"{database_name}.json", "r", encoding=encodingFormat) as db:
        convert = json.load(db)
    return convert[key]

def json_read_all():
    with open("main_database.json", "r", encoding=encodingFormat) as db:
        convert = json.load(db)
    print(json.dumps(convert, indent=2))
