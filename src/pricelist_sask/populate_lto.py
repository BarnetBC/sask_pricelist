#!/usr/bin/env python3
import psycopg2

DB_CONFIG = {
    'host': 'localhost',
    'database': 'bottlebridge',
    'user': 'olena',
    'password': 'Barnet359?',
}


def populate_lto() -> None:
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE pricelist_general pg
                SET lto = l.price_diff
                FROM lto l
                WHERE l.province = pg.province
                  AND l.cspcid = pg.cspcid
                  AND pg.price_date::date >= l.date_from
                  AND pg.price_date::date <= l.date_to
            """)
            updated = cursor.rowcount
        conn.commit()

    print(f'Updated {updated} rows in pricelist_general.lto.')


if __name__ == '__main__':
    populate_lto()
