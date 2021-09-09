import couchdb
import os
import sys
from src.scenarios import *
from dotenv import load_dotenv

load_dotenv()

# Load env vars
namespace = os.getenv('EKS_NAMESPACE')
couchdb_user = os.getenv('COUCHDB_USER')
couchdb_password = os.getenv('COUCHDB_PASSWORD')
db_names = [i for i in os.environ.get("COUCHDB_DB_NAMES").split(" ")]
couchserver = couchdb.Server(
    "http://%s:%s@localhost:5984/" % (couchdb_user, couchdb_password))
n_rows = int(os.getenv('COUCHDB_INSERT_ROWS'))


def main():
    args = sys.argv[1:]

    if len(args) == 2 and args[0] == '--scenario':
        scenario = int(args[1])
        print(f'scenario: {scenario}')
        if scenario == 1:
            scenario_1_delete_all_pods(
                couchserver, namespace, n_rows, db_names)

        elif scenario == 2:
            scenario_2_delete_some_pods(
                couchserver, namespace, n_rows, db_names)

        elif scenario == 3:
            clear_dbs(couchserver)

    else:
        raise Exception(
            "You must provide --scenario argument as first argument")


if __name__ == "__main__":
    main()
