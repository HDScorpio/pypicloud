from __future__ import unicode_literals
import logging
from pyramid.settings import aslist

from .base import IAccessBackend


LOG = logging.getLogger(__name__)


class RemoteUserAccessBackend(IAccessBackend):
    """
    This backend allows you to authenticate against a remote LDAP server.
    """

    @classmethod
    def configure(cls, settings):
        kwargs = super(RemoteUserAccessBackend, cls).configure(settings)
        kwargs['admins'] = aslist(settings.get('auth.admins', []))
        return kwargs

    def __init__(self, request=None, **kwargs):
        self.admins = kwargs.pop('admins')
        super(RemoteUserAccessBackend, self).__init__(request, **kwargs)

    def _get_password_hash(self, username):
        raise RuntimeError("REMOTE_USER should never call _get_password_hash")

    def verify_user(self, username, password):
        # Should never call
        return False

    def is_admin(self, username):
        if not username:
            return False
        return username in self.admins

    def user_data(self, username=None):
        if username is None:
            return []
        else:
            return {
                "username": username,
                "admin": self.is_admin(username),
                "groups": self.groups(username),
            }

    def groups(self, username=None):
        return []

    def group_members(self, group):
        return []

    def group_permissions(self, package):
        return {}

    def user_permissions(self, package):
        return {}

    def user_package_permissions(self, username):
        return []

    def group_package_permissions(self, group):
        return []

    def check_health(self):
        return True, ""
