import pytest
import smartsheet
import os.path
import time
import datetime

class TestProofs:
    # values go here

# Single proof tests
def test_get_proof(self, smart_setup):
        smart = smart_setup['smart']
        file = smart.Proofs.get_proof(
            smart_setup['sheet_b'].id,
            TestProofs.sheet_file_proof.id
        )
        assert file.name == 'stooges.jpg'






def test_delete_proof(self, smart_setup):

def test_create_proof(self, smart_setup):

def test_update_proof(self, smart_setup):

####################################################################
