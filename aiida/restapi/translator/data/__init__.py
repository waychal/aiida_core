# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################



from aiida.restapi.translator.node import NodeTranslator
import aiida

class DataTranslator(NodeTranslator):
    """
    Translator relative to resource 'data' and aiida class `~aiida.orm.data.Data`
    """

    # A label associated to the present class (coincides with the resource name)
    __label__ = "data"
    # The AiiDA class one-to-one associated to the present class
    _aiida_class = aiida.orm.data.Data
    # The string name of the AiiDA class
    _aiida_type = "data.Data"
    # The string associated to the AiiDA class in the query builder lexicon
    _qb_type = _aiida_type + '.'

    _result_type = __label__

    _default_projections = {
        "column_order": [
            "id",
            "label",
            "type",
            "ctime",
            "mtime",
            "uuid",
            "user_id",
            "user_email",
            "attributes",
            "extras"
        ],
        "column_info": {
            "id": {"is_display": True},
            "label": {"is_display": False},
            "type": {"is_display": True},
            "ctime": {"is_display": True},
            "mtime": {"is_display": True},
            "uuid": {"is_display": False},
            "user_id": {"is_display": False},
            "user_email": {"is_display": True},
            "attributes": {"is_display": False},
            "extra": {"is_display": False}
        }
    }

    def __init__(self,Class=None, **kwargs):
        """
        Initialise the parameters.
        Create the basic query_help
        """

        # Assume default class is this class (cannot be done in the
        # definition as it requires self)
        if Class is None:
            Class = self.__class__

        super(DataTranslator, self).__init__(Class=Class, **kwargs)
