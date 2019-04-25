# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.enum.loading_strategy
    -----------------------------------------------

    TODO doc

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from enum import Enum


class LoadingStrategy(Enum):
    """TODO doc
    """
    DEFAULT = 0
    LEAST_POPULATED = 1
    MOST_POPULATED = 2
