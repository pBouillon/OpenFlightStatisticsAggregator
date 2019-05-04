# -*- coding: utf-8 -*-
"""
    tests.dal.test_sql_bridge
    -------------------------

    Test suite for `dal.sql_bridge`.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from dataclasses import dataclass
from unittest import TestCase

from db_normalizer.dal.sql_bridge import Dal


class TestSqlBridge(TestCase):
    """References TestSqlBridge

    Test suite for the sql bridge toolbox.
    """

    def test_valid_dataclass_to_list(self):
        """
        """
        expected = [1, 'a']

        @dataclass
        class Dummy:
            attr1: int
            attr2: str

        actual = Dal.dataclass_to_list(Dummy(*expected))

        self.assertEqual(expected, actual)
