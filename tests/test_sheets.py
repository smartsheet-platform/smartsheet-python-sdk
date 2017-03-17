import pytest
import smartsheet

@pytest.mark.usefixtures("smart_setup")
class TestSheets:
    exec_share = None
    star_wars_sheet = None

    def test_list_sheets(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.list_sheets()
        sheets = action.result
        assert action.total_count > 0

    def test_copy_sheet(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.copy_sheet(
            smart_setup['sheet_b'].id,
            smart.models.ContainerDestination({
                'destination_id': smart_setup['folder'].id,
                'destination_type': 'folder',
                'new_name': 'pytest_fixture_sheetC'
            }),
            include='all'
        )
        new_sheet = action.result
        assert action.message == 'SUCCESS'

    def test_get_sheet_version(self, smart_setup):
        smart = smart_setup['smart']
        result = smart.Sheets.get_sheet_version(smart_setup['sheet'].id)
        assert result.request_response.status_code == 200
        assert isinstance(result, smart.models.version.Version)
        assert isinstance(result.version, int)

    def test_get_sheet_version_from_model(self, smart_setup):
        smart = smart_setup['smart']
        result = smart_setup['sheet'].get_version()
        assert result.request_response.status_code == 200
        assert isinstance(result, smart.models.version.Version)
        assert isinstance(result.version, int)

    @pytest.mark.xfail(raises=ValueError)
    def test_get_sheet_version_required_fields(self, smart_setup):
        smart = smart_setup['smart']
        result = smart.Sheets.get_sheet_version(None)

    def test_share_sheet(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet'].share(
            smart.models.Share({
                'access_level': 'EDITOR',
                'group_id': smart_setup['groups']['exec'].id
            })
        )
        share = action.result
        TestSheets.exec_share = share
        assert action.message == 'SUCCESS'

    def test_list_shares(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet'].shares()
        shares = action.result
        assert action.request_response.status_code == 200

    @pytest.mark.usefixtures('tmpdir')
    def test_get_sheet_as_pdf(self, smart_setup, tmpdir):
        smart = smart_setup['smart']
        action = smart.Sheets.get_sheet_as_pdf(
            smart_setup['sheet'].id,
            tmpdir.strpath
        )
        assert action.message == 'SUCCESS'

    @pytest.mark.usefixtures('tmpdir')
    def test_get_sheet_as_excel(self, smart_setup, tmpdir):
        smart = smart_setup['smart']
        action = smart.Sheets.get_sheet_as_excel(
            smart_setup['sheet'].id,
            tmpdir.strpath
        )
        assert action.message == 'SUCCESS'

    @pytest.mark.usefixtures('tmpdir')
    def test_get_sheet_as_csv(self, smart_setup, tmpdir):
        smart = smart_setup['smart']
        action = smart.Sheets.get_sheet_as_csv(
            smart_setup['sheet'].id,
            tmpdir.strpath,
            str(smart_setup['sheet'].id) + '.csv'
        )
        assert action.message == 'SUCCESS'

    def test_update_share(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet'].update_share(
            TestSheets.exec_share.id,
            smart.models.Share({
                'access_level': 'EDITOR_SHARE'
            })
        )
        TestSheets.exec_share = action.result
        assert action.message == 'SUCCESS'

    def test_get_share(self, smart_setup):
        smart = smart_setup['smart']
        share = smart_setup['sheet'].get_share(
            TestSheets.exec_share.id
        )
        TestSheets.exec_share = share
        assert share.request_response.status_code == 200
        assert isinstance(share, smart.models.share.Share)

    # on behalf of Moe, I try to make this change
    def test_update_sheet(self, smart_setup):
        smart = smartsheet.Smartsheet()
        smart.assume_user(smart_setup['users']['moe'].email)
        action = smart.Sheets.update_sheet(
            smart_setup['sheet'].id,
            smart.models.Sheet({
                'name': 'You knuckleheads!'
            })
        )
        assert isinstance(action, smart.models.error.Error)

    def test_delete_share(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet'].delete_share(
            TestSheets.exec_share.id
        )
        assert action.message == 'SUCCESS'

    def test_new_and_shared_sheet(self, smart_setup):
        smart = smartsheet.Smartsheet()
        newsheet = smart.models.Sheet({
            'name': 'pytest_social_sheet',
            'columns': [{
                'title': 'Primary',
                'primary': True,
                'type': 'TEXT_NUMBER'
            }]
        })
        action = smart.Folders.create_sheet_in_folder(
            smart_setup['folder'].id, newsheet);
        assert action.message == 'SUCCESS'
        newsheet = action.result
        action = newsheet.share(
            smart.models.Share({
                'accessLevel': 'ADMIN',
                'email': smart_setup['users']['moe'].email
            })
        )
        assert action.message == 'SUCCESS'
        share = action.result
        # now edit as Moe
        smart.assume_user(smart_setup['users']['moe'].email)
        action = newsheet.update_name('You knuckleheads!')
        assert action.message == 'ERROR'
        assert isinstance(action, smart.models.error.Error)
        assert action.result.code == 1004

    def test_get_publish_status(self, smart_setup):
        smart = smart_setup['smart']
        status = smart_setup['sheet_b'].get_publish_status()
        assert isinstance(status, smart.models.sheet_publish.SheetPublish)
        assert status.read_only_lite_enabled == False

    def test_set_publish_status(self, smart_setup):
        smart = smart_setup['smart']
        action = smart_setup['sheet_b'].set_publish_status(
            smart.models.SheetPublish({
                'read_only_lite_enabled': True,
                'read_only_full_enabled': True,
                'read_write_enabled': True
            })
        )
        assert action.message == 'SUCCESS'
        assert isinstance(action.result, smart.models.sheet_publish.SheetPublish)
        status = smart_setup['sheet_b'].get_publish_status()
        assert isinstance(status, smart.models.sheet_publish.SheetPublish)
        assert status.read_only_lite_enabled == True

    def test_get_sheet_by_name(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.Sheets.get_sheet_by_name(
            'pytest_fixture_sheet ' + smart_setup['now']
        )
        assert sheet.id == smart_setup['sheet'].id

    def test_get_column_by_title(self, smart_setup):
        smart = smart_setup['smart']
        col = smart.Sheets.get_column_by_title(
            smart_setup['sheet'].id,
            'The First Column'
        )
        assert col.id == smart_setup['sheet_primary_col'].id

    def test_list_org_sheets(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.list_org_sheets()
        assert action.total_count > 0

    def test_get_sheet_by_unknown_name(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.Sheets.get_sheet_by_name(
            'The Sheet Who Must Not Be Named'
        )
        assert sheet == False

    def test_send_sheet(self, smart_setup):
        smart = smart_setup['smart']
        action = smart.Sheets.send_sheet(
            smart_setup['sheet'].id,
            smart.models.SheetEmail({
                'send_to': smart.models.Recipient({
                    'email': 'john.doe@smartsheet.com'
                }),
                'subject': 'Get a load of this!',
                'format': 'PDF',
                'format_details': smart.models.FormatDetails({
                    'paper_size': 'WIDE'
                }),
                'message': 'You will love this.',
                'ccMe': False
            })
        )
        assert action.message == 'SUCCESS'

    def test_update_request(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.Sheets.get_sheet(smart_setup['sheet'].id)
        ids = []
        column_ids = []
        for row in sheet.rows:
            ids.append(row.id)
            for cell in row.cells:
                column_ids.append(cell.column_id)

        email = smart.models.MultiRowEmail()
        email.send_to = smart.models.Recipient({'email': 'john.doe@smartsheet.com'})
        email.row_ids = ids
        email.column_ids = list(set(column_ids))
        action = smart.Sheets.send_update_request(
            smart_setup['sheet'].id,
            email
        )
        assert action.message == 'SUCCESS'

    def test_search_sheet(self, smart_setup):
        smart = smart_setup['smart']
        result = smart.Sheets.search_sheet(
            smart_setup['sheet_b'].id,
            'Nike'
        )
        assert result.request_response.status_code == 200
        assert result.total_count >= 0
        assert isinstance(result, smart.models.search_result.SearchResult)

    def test_move_sheet(self, smart_setup):
        smart = smart_setup['smart']
        folder_name_b = 'pytestB ' + smart_setup['now']
        action = smart.Home.create_folder(folder_name_b)
        test_folder_b = action.result

        action = smart.Sheets.move_sheet(
            smart_setup['sheet'].id,
            smart.models.ContainerDestination({
                'destination_type': 'folder',
                'destination_id': test_folder_b.id
            })
        )
        assert action.message == 'SUCCESS'
    
    def test_complex_sheet(self, smart_setup):
        smart = smart_setup['smart']
        sheet = smart.models.Sheet({
            'name': 'star_wars',
            'columns': [{
                    'title': 'Favorite',
                    'type': 'CHECKBOX',
                    'symbol': 'STAR'
                }, {
                    'title': 'Title',
                    'primary': True,
                    'type': 'TEXT_NUMBER'
                }, {
                    'title': 'Year Released',
                    'type': 'TEXT_NUMBER',
                    'filter': smart.models.Filter({
                        'type': 'LIST',
                        'excludeSelected': False,
                        'values': [1977]
                    })
                }, {
                    'title': 'Characters Featured',
                    'type': 'PICKLIST',
                    'options': [
                        'Luke Skywalker',
                        'Han Solo',
                        'Anakin Skywalker',
                        'Yoda',
                        'Obi-Wan Kenobi',
                        'Qui-Gon Jinn',
                        'Jabba the Hutt',
                        'Greedo'
                    ]
                }, {
                    'title': 'AutoIncrement',
                    'type': 'TEXT_NUMBER',
                    'system_column_type': 'AUTO_NUMBER',
                    'auto_number_format': smart.models.AutoNumberFormat({
                        'starting_number': 1,
                        'fill': '00000',
                        'suffix': '_',
                        'prefix': '_'
                    })
                }, {
                    'title': 'Modified By',
                    'type': 'CONTACT_LIST',
                    'systemColumnType': 'MODIFIED_BY'
                }
            ]
        })
        
        col = sheet.get_column_by_title('AutoIncrement')
        col.auto_number_format.startingNumber = 1;

        action = smart.Folders.create_sheet_in_folder(
            smart_setup['folder'].id,
            sheet
        )
        sheet = action.result
        TestSheets.star_wars_sheet = sheet
        assert action.message == 'SUCCESS'
        
        rows = [smart.models.Row({
                'to_bottom': True,
                'cells': [
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Favorite').id,
                        'value': True
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Title').id,
                        'value': 'Star Wars Episode IV: A New Hope',
                        'format': ',,1,1,,,,,,,,,,,,'
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Year Released').id,
                        'value': 1977
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Characters Featured').id,
                        'value': 'Luke Skywalker'
                    })
                ]
            }), smart.models.Row({
                'to_bottom': True,
                'cells': [
                    smart.models.Cell({
                        'columnId': sheet.get_column_by_title('Favorite').id,
                        'value': True
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Title').id,
                        'value': 'Star Wars Episode V: The Empire Strikes Back',
                        'format': ',,1,1,,,,,,,,,,,,'
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Year Released').id,
                        'value': 1980
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Characters Featured').id,
                        'value': 'Han Solo'
                    })
                ]
            }), smart.models.Row({
                'to_bottom': True,
                'cells': [
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Favorite').id,
                        'value': False
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Title').id,
                        'value': 'Star Wars Episode VI: Return of the Jedi',
                        'format': ',,1,1,,,,,,,,,,,,'
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Year Released').id,
                        'value': 1983
                    }), 
                    smart.models.Cell({
                        'column_id': sheet.get_column_by_title('Characters Featured').id,
                        'value': 'Luke Skywalker'
                    })
                ]
            })]
    
        action = sheet.add_rows(rows)
        assert action.message == 'SUCCESS'
    
        
    