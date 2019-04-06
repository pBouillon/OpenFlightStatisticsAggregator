# -*- coding: utf-8 -*-
"""
    db_normalizer.dal.sql_bridge
    ----------------------------

    Bridge between the application and the Oracle database.

    /!\\ WiP /!\\

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
import cx_Oracle
import pandas as pd
from sqlalchemy import create_engine

from db_normalizer.dal.utils import ConnectionData

if __name__ == '__main__':
    oracle_connection_string = (
            'oracle+cx_oracle://{username}:{password}@' +
            cx_Oracle.makedsn(
                '{hostname}',
                '{port}',
                service_name='{service_name}'
            )
    )

    engine = create_engine(
        oracle_connection_string.format(
            username=ConnectionData.username,
            password=ConnectionData.password,
            hostname=ConnectionData.hostname,
            port=ConnectionData.port,
            service_name=ConnectionData.service_name,
        )
    )

    data = pd.read_sql("SELECT * FROM TEST", engine)
    print(data)
