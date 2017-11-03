import pytest
import smartsheet
from datetime import datetime
from dateutil.tz import *
import json
import os
import six

@pytest.fixture(scope="module")
def smart_setup(request):
    # set up a test session folder with basic starting points
    smart = smartsheet.Smartsheet()
    now = datetime.now(tzlocal()).strftime("%Y-%m-%d %H:%M:%S%Z")

    # test run base folders
    folder_name = 'pytest ' + now
    action = smart.Home.create_folder(folder_name)
    test_folder = action.result

    # add a sheet to mess around with
    sheet = smart.models.Sheet({
        'name': 'pytest_fixture_sheet ' + now,
        'columns': [{
            'title': 'The First Column',
            'primary': True,
            'type': 'TEXT_NUMBER'
        }, {
            'title': 'Favorite',
            'type': 'CHECKBOX',
            'symbol': 'STAR'
        }, {
            'title': 'Disposable',
            'type': 'TEXT_NUMBER'
        }]
    })
    action = smart.Folders.create_sheet_in_folder(test_folder.id, sheet);
    sheet = action.result

    # get primary column id
    for idx, col in enumerate(sheet.columns):
        if col.primary:
            break
    sheet_primary_col = col

    # add a row
    action = sheet.add_rows([smart.models.Row({
        'to_top': True,
        'cells': [{
            'column_id': sheet_primary_col.id,
            'value': 'The first column of the first row.'
        }]
    })])
    sheet = smart.Sheets.get_sheet(sheet.id)

    sheet_b = smart.models.Sheet({
        'name': 'pytest_fixture_sheetB ' + now,
        'columns': [{
            'title': 'Brand',
            'primary': True,
            'type': 'TEXT_NUMBER'
        }]
    })
    action = smart.Folders.create_sheet_in_folder(test_folder.id, sheet_b);
    sheet_b = action.result
    for idx, col in enumerate(sheet_b.columns):
        if col.primary:
            break
    sheet_b_primary_col = col

    action = sheet_b.add_rows([
        smart.models.Row({
            'to_top': True,
            'cells': [{
                'column_id': sheet_b_primary_col.id,
                'value': 'Nike'
            }]
        }),
        smart.models.Row({
            'to_top': True,
            'cells': [{
                'column_id': sheet_b_primary_col.id,
                'value': 'Google'
            }]
        }),
        smart.models.Row({
            'to_top': True,
            'cells': [{
                'column_id': sheet_b_primary_col.id,
                'value': 'Adidas'
            }]
        }),
        smart.models.Row({
            'to_top': True,
            'cells': [{
                'column_id': sheet_b_primary_col.id,
                'value': 'Keen'
            }]
        })])
    rows = action.result
    sheet_b = smart.Sheets.get_sheet(sheet_b.id)

    users = os.environ.get('SMARTSHEET_FIXTURE_USERS', None)
    users = json.loads(users)
    fixusers = {}
    for nick,info in six.iteritems(users):
        profile = smart.Users.get_user(info['id'])
        fixusers[nick] = profile
    action = smart.Groups.list_groups(include_all=True)
    grps = action.result
    groups = {}
    need_exec = True
    for gp in grps:
        groups[gp.name] = gp
        if gp.name == 'exec':
            need_exec = False

    if need_exec:
        group = smart.models.Group({
            'name': 'exec',
            'members': [
                smart.models.GroupMember({
                    'email': fixusers['moe'].email
                }),
                smart.models.GroupMember({
                    'email': fixusers['admin'].email
                })
            ]
        })
        action = smart.Groups.create_group(group)
        assert action.message == 'SUCCESS'

    fixture = {
        'smart': smart,
        'folder': test_folder,
        'sheet': sheet,
        'sheet_primary_col': sheet_primary_col,
        'sheet_b': sheet_b,
        'sheet_b_primary_col': sheet_b_primary_col,
        'now': now,
        'users': fixusers,
        'groups': groups
    }

    def smart_teardown():
        action = fixture['smart'].Sheets.delete_sheet(fixture['sheet'].id)
        if action.message == 'SUCCESS':
            print("deleted fixture sheet")
        action = fixture['smart'].Sheets.delete_sheet(fixture['sheet_b'].id)
        if action.message == 'SUCCESS':
            print("deleted fixture sheet_b")
        action = fixture['smart'].Folders.delete_folder(fixture['folder'].id)
        if action.message == 'SUCCESS':
            print("deleted fixture folder")

    request.addfinalizer(smart_teardown)
    return fixture
