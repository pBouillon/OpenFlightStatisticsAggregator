# -*- coding: utf-8 -*-
"""
    db_normalizer.data_loader.enum.loading_strategy
    -----------------------------------------------

    Define the loading strategy to be used for the external data loading

    :authors: Bouillon Pierre, Cesari Alexandre.
    :licence: MIT, see LICENSE for more details.
"""
from enum import Enum


class LoadingStrategy(Enum):
    """Loading strategy elements to be used for the external data loading
    """
    DEFAULT = 0
    LEAST_POPULATED = 1
    MOST_POPULATED = 2
