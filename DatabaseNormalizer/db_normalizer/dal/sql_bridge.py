import cx_Oracle

from db_normalizer.sql_utils.utils import ConnectionData


if __name__ == '__main__':
    connection = cx_Oracle.connect(
        user=ConnectionData.login,
        password=ConnectionData.password,

    )

    cursor = connection.cursor()
