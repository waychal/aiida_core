# -*- coding: utf-8 -*-
###########################################################################
# Copyright (c), The AiiDA team. All rights reserved.                     #
# This file is part of the AiiDA code.                                    #
#                                                                         #
# The code is hosted on GitHub at https://github.com/aiidateam/aiida_core #
# For further information on the license, see the LICENSE.txt file        #
# For further information please visit http://www.aiida.net               #
###########################################################################

import abc

from aiida.common.hashing import is_password_usable
from aiida.common import exceptions

__all__ = ['User', 'UserCollection']


class UserCollection(object):
    """
    The collection of users stored in a backend
    """

    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def create(self, email):
        """
        Create a user with the provided email address

        :param email: An email address for the user
        :return: A new user object
        :rtype: :class:`User`
        """
        pass

    def find(self, email=None, id=None):
        """
        Final all users matching the given criteria
        :param email: An email address to search for
        :return: A collection of users matching the criteria
        """
        from .querybuilder import QueryBuilder

        qb = QueryBuilder()
        qb.append(User, filters={'email': {'==': email}})
        res = [_[0] for _ in qb.all()]
        if res is None:
            return []

        return res

    def get(self, email):
        results = self.find(email=email)
        if not results:
            raise exceptions.NotExistent()
        else:
            if len(results) > 1:
                raise exceptions.MultipleObjectsError()
            else:
                return results[0]

    def get_automatic_user(self):
        from aiida.common.utils import get_configured_user_email

        email = get_configured_user_email()
        if not email:
            return None

        try:
            return self.get(email)
        except (exceptions.MultipleObjectsError, exceptions.NotExistent):
            return None

    def all(self):
        """
        Final all users matching the given criteria
        :param email:
        :return: A collection of users matching the criteria
        """
        from .querybuilder import QueryBuilder

        qb = QueryBuilder()
        qb.append(User)
        return [_[0] for _ in qb.all()]


class User(object):
    """
    This is the base class for User information in AiiDA.  An implementing
    backend needs to provide a concrete version.
    """
    REQUIRED_FIELDS = ['first_name', 'last_name', 'institution']

    __metaclass__ = abc.ABCMeta

    def __init__(self, backend):
        self._backend = backend

    @property
    def backend(self):
        return self._backend

    @abc.abstractproperty
    def pk(self):
        pass

    @abc.abstractproperty
    def id(self):
        pass

    @abc.abstractproperty
    def is_stored(self):
        """
        Is the user stored

        :return: True if stored, False otherwise
        :rtype: bool
        """
        pass

    @abc.abstractmethod
    def store(self):
        pass

    @abc.abstractproperty
    def email(self):
        pass

    @abc.abstractmethod
    @email.setter
    def email(self, val):
        pass

    @property
    def password(self):
        return self._get_password()

    @password.setter
    def password(self, val):
        from aiida.common.hashing import create_unusable_pass, pwd_context

        if val is None:
            pass_hash = create_unusable_pass()
        else:
            pass_hash = pwd_context.encrypt(val)

        self._set_password(pass_hash)

    @abc.abstractmethod
    def _get_password(self):
        pass

    @abc.abstractmethod
    def _set_password(self, new_pass):
        pass

    @abc.abstractproperty
    def first_name(self):
        pass

    @abc.abstractmethod
    @first_name.setter
    def first_name(self, val):
        pass

    @abc.abstractproperty
    def last_name(self):
        pass

    @abc.abstractmethod
    @last_name.setter
    def last_name(self, val):
        pass

    @abc.abstractproperty
    def institution(self):
        pass

    @abc.abstractmethod
    @institution.setter
    def institution(self, val):
        pass

    @abc.abstractproperty
    def is_active(self):
        pass

    @abc.abstractmethod
    @is_active.setter
    def is_active(self, val):
        pass

    @abc.abstractproperty
    def last_login(self):
        pass

    @abc.abstractmethod
    @last_login.setter
    def last_login(self, val):
        pass

    @abc.abstractproperty
    def date_joined(self):
        pass

    @abc.abstractmethod
    @date_joined.setter
    def date_joined(self, val):
        pass

    def has_usable_password(self):
        return is_password_usable(self._get_password())

    def get_full_name(self):
        """
        Return the user full name

        :return: the user full name
        """
        if self.first_name and self.last_name:
            return "{} {} ({})".format(self.first_name, self.last_name,
                                       self.email)
        elif self.first_name:
            return "{} ({})".format(self.first_name, self.email)
        elif self.last_name:
            return "{} ({})".format(self.last_name, self.email)
        else:
            return "{}".format(self.email)

    def get_short_name(self):
        """
        Return the user short name (typically, this returns the email)

        :return: The short name
        """
        return self.email

    @staticmethod
    def get_db_columns():
        """
        This method returns a list with the column names and types of the table
        corresponding to this class.
        :return: a list with the names of the columns
        """
        print "in orm user abstract"
        pass

    @staticmethod
    def get_db_columns_help_text():
        """
        :return: dict of help text for every column
        """
        print "get help text from here.."
        return {
            "first_name": {
                "help_text": "First name of the user",
                "display_name": "First name"
            },
            "last_name": {
                "help_text": "Last name of the user",
                "display_name": "Last name"
            },
            "email": {
                "help_text": "e-mail of the user",
                "display_name": "email"
            },
            "institution": {
                "help_text": "Affiliation of the user",
                "display_name": "Institution"
            },
            "date_joined": {
                "help_text": "Date and time of registration",
                "display_name": "User since"
            },
            "last_login": {
                "help_text": "Date and time of the last login",
                "display_name": "Last login"
            },
            "is_active": {
                "help_text": "True(False) if the user is active(not)",
                "display_name": "Active"
            },
            "user_id": {
                "help_text": "Id of the user that created the node",
                "display_name": "Id of creator"
            },
            "user_email": {
                "help_text": "Email of the user that created the node",
                "display_name": "Email of creator"
            }
        }
