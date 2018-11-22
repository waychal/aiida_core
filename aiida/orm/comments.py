# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################
"""Comment objects and functions"""
from __future__ import division
from __future__ import print_function
from __future__ import absolute_import

from . import backends
from . import entities
from . import users

__all__ = ('Comment',)


class Comment(entities.Entity):
    """Base class to map a DbComment that represents a comment attached to a certain Node."""

    class Collection(entities.Collection):
        """The collection of Comment entries."""

        def delete(self, comment):
            """
            Remove a Comment from the collection with the given id

            :param comment: the id of the comment to delete
            """
            self._backend.comments.delete(comment)

        def get(self, comment):
            """
            Return a Comment given its id

            :param comment: the id of the comment to retrieve
            :return: the comment
            :raise NotExistent: if the comment with the given id does not exist
            :raise MultipleObjectsError: if the id cannot be uniquely resolved to a comment
            """
            return self._backend.comments.get(comment)

    def __init__(self, node, user, content=None, backend=None):
        """
        Create a Comment for a given node and user

        :param node: a Node instance
        :param user: a User instance
        :param content: the comment content
        :return: a Comment object associated to the given node and user
        """
        backend = backend or backends.construct_backend()
        model = backend.comments.create(node=node, user=user.backend_entity, content=content)
        super(Comment, self).__init__(model)

    def __str__(self):
        arguments = [self.uuid, self.node.pk, self.user.email, self.content]
        return 'Comment<{}> for node<{}> and user<{}>: {}'.format(*arguments)

    @property
    def ctime(self):
        return self._backend_entity.ctime

    @property
    def mtime(self):
        return self._backend_entity.mtime

    def set_mtime(self, value):
        return self._backend_entity.set_mtime(value)

    @property
    def node(self):
        return self._backend_entity.node

    @property
    def user(self):
        return users.User.from_backend_entity(self._backend_entity.user)

    def set_user(self, value):
        self._backend_entity.set_user(value.backend_entity)

    @property
    def content(self):
        return self._backend_entity.content

    def set_content(self, value):
        return self._backend_entity.set_content(value)
