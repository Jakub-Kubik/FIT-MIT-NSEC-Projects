#!/usr/bin/env python

from scraper_funcs import connect_to_db, create_and_switch_to_db
from scraper_save_data import (
    save_group_1_to_db,
    save_group_2_to_db,
    save_group_3_to_db,
    save_group_4_to_db,
    save_group_5_to_db,
)

data_groups = {
    "group_1": {
        "hospitalizace": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/hospitalizace.csv",
        "nakazeni-vyleceni-umrti-testy": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/nakazeni-vyleceni-umrti-testy.csv",
    },
    "group_2": {
        "kraj-okres-nakazeni-vyleceni-umrti": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-nakazeni-vyleceni-umrti.csv",
        "obyvatelstvo": "https://www.czso.cz/documents/62353418/143522504/130142-21data043021.csv",
    },
    "group_3": {
        "ockovani-umrti": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-umrti.csv",
        "ockovani-pozitivni": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani-pozitivni.csv",
    },
    "group_4": {
        "kraj-okres-testy": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/kraj-okres-testy.csv",
    },
    "group_5": {
        "ockovani": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/ockovani.csv",
        "osoby": "https://onemocneni-aktualne.mzcr.cz/api/v2/covid-19/osoby.csv",
    }
}


def main():
    upa_proj_db = "covid-19"
    client = connect_to_db()

    create_and_switch_to_db(client, upa_proj_db)

    save_group_1_to_db(client, data_groups["group_1"])

    save_group_2_to_db(client, data_groups["group_2"])

    save_group_3_to_db(client, data_groups["group_3"])

    save_group_4_to_db(client, data_groups["group_4"])

    # save_group_5_to_db(client, data_groups["group_5"])


if __name__ == "__main__":
    main()