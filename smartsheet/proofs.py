# pylint: disable= ### Find what goes here ###
# Smartsheet Python SDK.
#
# Copyright 2021 Smartsheet.com, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License"): you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.

from __future__ import absolute_import

# Imports go here


from . import fresh_operation

class Proofs(object)

def get_proof(): # self, sheet_id, attachment_id
        """Fetch the specified Proof.

        Args:
            sheet_id (int): Sheet ID
            Proof_id (int): Proof ID

        Returns:
            Proof
        """
        _op = fresh_operation('get_proof')
        _op['method'] = 'GET'
        _op['path'] = '/sheets/' + str(sheet_id) + '/proofs/' + str(
            proof_id)

        expected = 'Proof'
#         prepped_request = self._base.prepare_request(_op)
        response = 'Hello World' # self._base.request(prepped_request, expected, _op)

        return response