import json
import os

import docopt
import pkg_resources

import six

import dcoscli
from dcos import (cmds, config, emitting, errors,
                  http, mesos, packagemanager, ssh_util, subprocess, util)

from dcos.errors import DCOSException, DefaultError
from dcoscli import tables
from dcoscli.subcommand import default_command_info, default_doc
from dcoscli.util import confirm, confirm_text, decorate_docopt_usage

logger = util.get_logger(__name__)

emitter = emitting.FlatEmitter()


def main(argv):
    try:
        return _main(argv)
    except DCOSException as e:
        emitter.publish(e)
        return 1


@decorate_docopt_usage
def _main(argv):
    args = docopt.docopt(
        default_doc("resource"),
        argv=argv,
        version='dcos-resource version {}'.format(dcoscli.version))
    http.silence_requests_warnings()

    return cmds.execute(_cmds(), args)


def _cmds():
    """
    :returns: All of the supported commands
    :rtype: dcos.cmds.Command
    """

    return [

        cmds.Command(
            hierarchy=['resource', '--info'],
            arg_keys=[],
            function=_resource),

        cmds.Command(
            hierarchy=['resource', 'quota'],
            arg_keys=['--json'],
            function=_quota),

        cmds.Command(
            hierarchy=['resource'],
            arg_keys=['--json'],
            function=_roles)
    ]


def _resource(info):
    """
    :param config_schema: Whether to output the config schema
    :type config_schema: boolean
    :param info: Whether to output a description of this subcommand
    :type info: boolean
    :returns: Process status
    :rtype: int
    """
    emitter.publish(default_command_info("resource"))
    return 0

# def _list(json_):
#     """List DC/OS resources
#
#     :param json_: If true, output json.
#         Otherwise, output a human readable table.
#     :type json_: bool
#     :rtype: int
#     """
#
#     client = mesos.DCOSClient()
#     masters = mesos.MesosDNSClient().masters()
#     master_state = client.get_master_state()
#
#     emitter.publish(master_state)

def _quota(json_):
    """List DC/OS quota

    :param json_: If true, output json.
        Otherwise, output a human readable table.
    :type json_: bool
    :rtype: int
    """

    client = mesos.DCOSClient()
    masters = mesos.MesosDNSClient().masters()
    roles = client.get_roles()

    if json_:
        emitter.publish(roles)
    else:
        table = tables.resource_quota_table(roles['roles'])
        output = six.text_type(table)
        if output:
            emitter.publish(output)
        else:
            emitter.publish(errors.DefaultError('No Roles found.'))

def _roles(json_):
    """List DC/OS roles

    :param json_: If true, output json.
        Otherwise, output a human readable table.
    :type json_: bool
    :rtype: int
    """

    client = mesos.DCOSClient()
    masters = mesos.MesosDNSClient().masters()
    roles = client.get_roles()

    if json_:
        emitter.publish(roles)
    else:
        table = tables.resource_roles_table(roles['roles'])
        output = six.text_type(table)
        if output:
            emitter.publish(output)
        else:
            emitter.publish(errors.DefaultError('No Roles found.'))
