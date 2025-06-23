import logging
import atexit

from fabric import Connection, SerialGroup, ThreadingGroup, runners
from invoke import Context
from fabric.exceptions import GroupException

import pprint
pp = pprint.PrettyPrinter(indent=2, width=120)


logger = logging.getLogger(__name__)

# Connection cache
_connections = {}

def _check_cached_connection(host=None):
    return _cache_connection(host)

def _cache_connection(host=None, connection=None):
    key = host if host else 'local'
    
    if connection is None:
        return _connections.get(key, None)
    
    _connections[key] = connection
    return _connections[key]

def _close_connections():
    for conn in _connections.values():
        if isinstance(conn, (SerialGroup, ThreadingGroup)):
            conn.close()
    _connections.clear()

atexit.register(_close_connections)

def run_cmd(command, hosts=None, parallel=False):
    result = {}

    if not hosts:
        result['local'] = Context().run(f'/bin/bash -l -c "{command}"', hide=True, warn=True)
    else:
        servers = []

        for host in hosts:
            ctx = _check_cached_connection(host)
        
            if ctx is not None:
                servers.append(ctx)
            else:
                servers.append(_cache_connection(host, Connection(host=host)))

        if parallel:
            ctx = ThreadingGroup().from_connections(servers)
        else:
            ctx = SerialGroup().from_connections(servers)
        
        del servers

        try:
            result = ctx.run(command, hide=True, warn=True, shell='/bin/bash -l -c')
        except GroupException as e:
            result = e.result

    if len(result) == 1:
        host = next(iter(result))
        return result[host].stdout.strip(), result[host].stderr.strip(), result[host].exited
    else:
        stdout, stderr, exit_codes = {}, {}, {}

        for key in result.keys():
            hostname = key.host

            if isinstance(result[key], runners.Result):
                stdout[hostname] = result[key].stdout.strip()
                stderr[hostname] = result[key].stderr.strip()
                exit_codes[hostname] = result[key].exited
            else:
                stdout[hostname] = ''
                stderr[hostname] = result[key]
                exit_codes[hostname] = next(iter(result[key].errors.values())).errno

        return stdout, stderr, exit_codes
