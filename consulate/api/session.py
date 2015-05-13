"""
Consul Session Endpoint Access

"""
from consulate.api import base


class Session(base.Endpoint):
    """Create, destroy, and query Consul sessions."""

    def create(self, name=None, behavior='release', node=None, delay=None,
               ttl=None, checks=None, datacenter=None):
        """Initialize a new session.

        None of the fields are mandatory, and in fact no body needs to be PUT
        if the defaults are to be used.

        Name can be used to provide a human-readable name for the Session.

        Behavior can be set to either ``release`` or ``delete``. This controls
        the behavior when a session is invalidated. By default, this is
        release, causing any locks that are held to be released. Changing this
        to delete causes any locks that are held to be deleted. delete is
        useful for creating ephemeral key/value entries.

        Node must refer to a node that is already registered, if specified.
        By default, the agent's own node name is used.

        LockDelay (``delay``) can be specified as a duration string using a
        "s" suffix for seconds. The default is 15s.

        The TTL field is a duration string, and like LockDelay it can use "s"
        as a suffix for seconds. If specified, it must be between 10s and
        3600s currently. When provided, the session is invalidated if it is
        not renewed before the TTL expires. See the session internals page
        for more documentation of this feature.

        Checks is used to provide a list of associated health checks. It is
        highly recommended that, if you override this list, you include the
        default "serfHealth".

        By default, the agent's local datacenter is used and you can specify
        another datacenter, However, it is not recommended to use
        cross-datacenter sessions.

        :param str name: A human readable session name
        :param str behavior: One of ``release`` or ``delete``
        :param str node: A node to create the session on
        :param str delay: A lock delay for the session
        :param str ttl: The time to live for the session
        :param lists checks: A list of associated health checks
        :param str datacenter: The datacenter to create the session on
        :return str: session ID

        """
        payload = {'name': name} if name else {}
        query_param = {'dc': datacenter} if datacenter else {}
        if node:
            payload['Node'] = node
        if behavior:
            payload['Behavior'] = behavior
        if delay:
            payload['LockDelay'] = delay
        if ttl:
            payload['TTL'] = ttl
        if checks:
            payload['Checks'] = checks
        return self._put_response_body(['create'], query_param,
                                       payload).get('ID')

    def destroy(self, session_id, datacenter=None):
        """Destroy an existing session

        :param str session_id: The session to destroy
        :return: bool

        """
        query_param = {'dc': datacenter} if datacenter else {}
        return self._put_no_response_body(['destroy', session_id], query_param)

    def info(self, session_id, datacenter=None):
        """Returns the requested session information within a given datacenter.
        By default, the datacenter of the agent is queried.

        :param str session_id: The session to get info about
        :return: dict

        """
        query_param = {'dc': datacenter} if datacenter else {}
        return self._get_response_body(['info', session_id], query_param)

    def list(self, datacenter=None):
        """Returns the active sessions for a given datacenter.

        :return: list

        """
        query_param = {'dc': datacenter} if datacenter else {}
        return self._get_response_body(['list'], query_param)

    def node(self, node, datacenter=None):
        """Returns the active sessions for a given node and datacenter.
        By default, the datacenter of the agent is queried.

        :param str node: The node to get active sessions for
        :return: list

        """
        query_param = {'dc': datacenter} if datacenter else {}
        return self._get_response_body(['node', node], query_param)

    def renew(self, session_id, datacenter=None):
        """Renew the given session. This is used with sessions that have a TTL,
        and it extends the expiration by the TTL. By default, the datacenter
        of the agent is queried.

        :param str session_id: The session to renew
        :return: dict

        """
        query_param = {'dc': datacenter} if datacenter else {}
        return self._put_response_body(['renew', session_id], query_param)

