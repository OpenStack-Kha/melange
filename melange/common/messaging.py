# vim: tabstop=4 shiftwidth=4 softtabstop=4

# Copyright 2011 OpenStack LLC.
# All Rights Reserved.
#
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import logging

import kombu.connection

from melange.common import config
from melange.common import utils


LOG = logging.getLogger('melange.common.messaging')


class Queue(object):

    def __init__(self, name):
        self.name = name

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()

    def connect(self):
        options = queue_connection_options("ipv4_queue")
        LOG.info("Connecting to message queue.")
        LOG.debug("Message queue connect options: %(options)s" % locals())
        self.conn = kombu.connection.BrokerConnection(**options)

    def put(self, msg):
        queue = self.conn.SimpleQueue(self.name, no_ack=True)
        LOG.debug("Putting message '%(msg)s' on queue '%(queue)s'" % locals())
        queue.put(msg)

    def close(self):
        LOG.info("Closing connection to message queue.")
        self.conn.close()


def queue_connection_options(queue_type):
    queue_params = config.Config.get_params_group(queue_type)
    queue_params['ssl'] = utils.bool_from_string(queue_params.get('ssl',
                                                                  "false"))
    queue_params['port'] = int(queue_params.get('port', 5672))

    return queue_params
