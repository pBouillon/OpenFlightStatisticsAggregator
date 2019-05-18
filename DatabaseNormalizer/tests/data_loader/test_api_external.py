# -*- coding: utf-8 -*-
"""
    tests.data_loader.test_api_external
    -----------------------------------

    Test suite for `db_normalizer.data_loader.test_api_external`.

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""

from unittest import TestCase

from db_normalizer.data_loader.api_external import url_encode


class TestApiExternal(TestCase):
    """References TestApiExternal

    Test suite for the api_external toolbox.
    """

    def test_valid_url_encode_closing_parenthesis_encoding(self):
        """A URL with closing parenthesises should be normalized
        """
        # arrange
        raw = 'a)url)with)closing)parenthesis'
        expected = raw.replace(')', '%29')

        # act
        actual = url_encode(raw)

        # assert
        self.assertEqual(
            expected,
            actual
        )

    def test_valid_url_encode_comma_encoding(self):
        """A URL with commas should be normalized
        """
        # arrange
        raw = 'a,simple,url,with,comma'
        expected = raw.replace(',', '%B4')

        # act
        actual = url_encode(raw)

        # assert
        self.assertEqual(
            expected,
            actual
        )

    def test_valid_url_encode_mixed_encoding(self):
        """A URL with mixed chars to encode should be normalized
        """
        # arrange
        raw = 'a url(with) mixed,\'encoding\''
        expected = raw.replace(
            ' ', '%20'
        ).replace(
            ',', '%B4'
        ).replace(
            '\'', '%27'
        ).replace(
            '(', '%28'
        ).replace(
            ')', '%29'
        )

        # act
        actual = url_encode(raw)

        # assert
        self.assertEqual(
            expected,
            actual
        )

    def test_valid_url_encode_no_need_to_format(self):
        """A URL that doesn't need to be encoded shouldn't be
        """
        # arrange
        expected = 'SimpleUrl'

        # act
        actual = url_encode(expected)

        # assert
        self.assertEqual(
            expected,
            actual
        )

    def test_valid_url_encode_opening_parenthesis_encoding(self):
        """A URL with opening parenthesises should be normalized
        """
        # arrange
        raw = 'a(url(with(opening(parenthesis'
        expected = raw.replace('(', '%28')

        # act
        actual = url_encode(raw)

        # assert
        self.assertEqual(
            expected,
            actual
        )

    def test_valid_url_encode_simple_quote_encoding(self):
        """A URL with simple quotes should be normalized
        """
        # arrange
        raw = 'a\'simple\'quoted\'url'
        expected = raw.replace('\'', '%27')

        # act
        actual = url_encode(raw)

        # assert
        self.assertEqual(
            expected,
            actual
        )

    def test_valid_url_encode_spaces(self):
        """A URL with spaces should be normalized
        """
        # arrange
        raw = 'a simple url with spaces'
        expected = raw.replace(' ', '%20')

        # act
        actual = url_encode(raw)

        # assert
        self.assertEqual(
            expected,
            actual
        )
