# pylint: disable=C0103,W0232

import pytest
from smartsheet.models import (
    AlternateEmail, Attachment, Column, Comment, ContainerDestination, CrossSheetReference,
    Discussion, ExplicitNull, Favorite, FormatDetails, Group, ImageUrl, MultiRowEmail, Recipient,
    Row, Schedule, Share, Sheet, SheetEmail, UpdateRequest, User, Workspace
)
from smartsheet.models.object_value import DURATION

from mock_api_test_helper import MockApiTestHelper, clean_api_error

class TestMockSerialization(MockApiTestHelper):
    @clean_api_error
    def test_attachment_serialization(self):
        self.client.as_test_scenario('Serialization - Attachment')

        url_spec = Attachment({
            'name': 'Search Engine',
            'description': 'A popular search engine',
            'attachmentType': 'LINK',
            'url': 'http://www.google.com'
        })

        response = self.client.Attachments.attach_url_to_sheet(1, url_spec)

        assert response.result.id == 2

    @clean_api_error
    def test_home_deserialization(self):
        self.client.as_test_scenario('Serialization - Home')

        home = self.client.Home.list_all_contents()

        assert home.sheets[0].name == 'editor share sheet'
        assert home.folders[0].name == 'empty folder'
        assert home.reports[0].name == 'admin report'
        assert home.sights[0].name == 'sight'
        assert home.workspaces[0].name == 'workspace'
        assert home.workspaces[0].sheets[0].name == 'workspace sheet'
        assert home.workspaces[0].folders[0].name == 'workspace folder'
        assert home.workspaces[0].folders[0].sheets[0].name == 'workspace folder sheet'
        assert home.workspaces[0].folders[0].folders[0].name == 'workspace folder folder'
        assert (home.workspaces[0].folders[0].folders[0].sheets[0].name
                == 'workspace folder folder sheet')

    @clean_api_error
    def test_group_serialization(self):
        self.client.as_test_scenario('Serialization - Groups')

        response = self.client.Groups.create_group(
            Group({
                'name': 'mock api test group',
                'description': "it's a group",
                'members': [
                    {
                        'email': 'john.doe@smartsheet.com'
                    },
                    {
                        'email': 'jane.doe@smartsheet.com'
                    }
                ]
            })
        )

        assert response.result.members[0].email == 'john.doe@smartsheet.com'

    @clean_api_error
    def test_discussion_serialization(self):
        self.client.as_test_scenario('Serialization - Discussion')

        response = self.client.Discussions.create_discussion_on_row(
            1,
            2,
            Discussion({
                'comment': Comment({
                    'text': 'This is a comment!'
                })
            })
        )

        assert response.result.comments[0].created_by.email == 'john.doe@smartsheet.com'

    @clean_api_error
    def test_contact_serialization(self):
        self.client.as_test_scenario('Serialization - Contact')

        contact = self.client.Contacts.get_contact('ABC')

        assert contact.email == 'john.doe@smartsheet.com'

    @clean_api_error
    def test_folder_serialization(self):
        self.client.as_test_scenario('Serialization - Folder')

        response = self.client.Home.create_folder('folder')

        assert response.result.name == 'folder'

    @clean_api_error
    def test_column_serialization(self):
        pytest.skip('Skipping until mock API test is updated')
        self.client.as_test_scenario('Serialization - Column')

        column = Column({
            'title': 'A Brave New Column',
            'type': 'PICKLIST',
            'options': [
                'option1',
                'option2',
                'option3'
            ],
            'index': 2,
            'validation': False,
            'width': 42,
            'locked': False
        })

        response = self.client.Sheets.add_columns(1, column)

        assert response.result.title == 'A Brave New Column'

    @clean_api_error
    def test_user_profile_serialization(self):
        self.client.as_test_scenario('Serialization - UserProfile')

        user_profile = self.client.Users.get_current_user()

        assert user_profile.account.name == 'john.doe@smartsheet.com'

    @clean_api_error
    def test_workspace_serialization(self):
        self.client.as_test_scenario('Serialization - Workspace')

        response = self.client.Workspaces.create_workspace(
            Workspace({
                'name': 'A Whole New Workspace'
            })
        )

        assert response.result.name == 'A Whole New Workspace'

    @clean_api_error
    def test_user_serialization(self):
        self.client.as_test_scenario('Serialization - User')

        response = self.client.Users.add_user(
            User({
                'email': 'john.doe@smartsheet.com',
                'admin': False,
                'licensedSheetCreator': True,
                'firstName': 'John',
                'lastName': 'Doe',
                'groupAdmin': False,
                'resourceViewer': True
            })
        )

        assert response.result.profile_image.image_id == 'abc'

    @clean_api_error
    def test_sheet_serialization(self):
        self.client.as_test_scenario('Serialization - Sheet')

        response = self.client.Home.create_sheet(
            Sheet({
                'name': 'The First Sheet',
                'columns': [
                    {
                        'title': 'The First Column',
                        'primary': True,
                        'type': 'TEXT_NUMBER'
                    },
                    {
                        'title': 'The Second Column',
                        'primary': False,
                        'type': 'TEXT_NUMBER',
                        'systemColumnType': 'AUTO_NUMBER',
                        'autoNumberFormat': {
                            'prefix': '{YYYY}-{MM}-{DD}-',
                            'suffix': '-SUFFIX',
                            'fill': '000000'
                        }
                    }
                ]
            })
        )

        assert response.result.columns[0].id == 2
        assert response.result.columns[1].auto_number_format.suffix == '-SUFFIX'

    @clean_api_error
    def test_alternate_email_serialization(self):
        self.client.as_test_scenario('Serialization - AlternateEmail')

        alt_email = AlternateEmail({
            'email': 'not.not.john.doe@smartsheet.com'
        })

        response = self.client.Users.add_alternate_email(1, [alt_email])

        assert response.result[0].email == 'not.not.john.doe@smartsheet.com'

    @clean_api_error
    def test_predecessor_serialization(self):
        pytest.skip('Skipping until mock API test is updated')
        self.client.as_test_scenario('Serialization - Predecessor')

        row = Row()
        row.cells.append({
            'columnId': 2,
            'objectValue': {
                'objectType': 'PREDECESSOR_LIST',
                'predecessors': [
                    {
                        'rowId': 3,
                        'type': 'FS',
                        'lag': {
                            'objectType': 'DURATION',
                            'negative': False,
                            'elapsed': False,
                            'weeks': 1.5,
                            'days': 2.5,
                            'hours': 3.5,
                            'minutes': 4.5,
                            'seconds': 5.5,
                            'milliseconds': 6
                        }
                    }
                ]
            }
        })

        response = self.client.Sheets.add_rows(1, row)

        assert response.result.cells[4].object_value.predecessors[0].lag.object_type == DURATION

    @clean_api_error
    def test_index_result_serialization(self):
        self.client.as_test_scenario('Serialization - IndexResult')

        response = self.client.Users.list_users()

        assert response.data[0].email == 'john.doe@smartsheet.com'

    @clean_api_error
    def test_image_serialization(self):
        self.client.as_test_scenario('Serialization - Image')

        row = self.client.Sheets.get_row(1, 2)

        assert row.cells[0].image.alt_text == 'puppy.jpg'

    @clean_api_error
    def test_image_urls_serialization(self):
        self.client.as_test_scenario('Serialization - Image Urls')

        response = self.client.Images.get_image_urls(ImageUrl({
            'imageId': 'abc',
            'height': 100,
            'width': 200
        }))

        assert response.image_urls[0].image_id == 'abc'

    @clean_api_error
    def test_bulk_failure_serialization(self):
        self.client.as_test_scenario('Serialization - BulkFailure')

        row1 = Row()
        row1.to_bottom = True
        row1.cells.append({
            'columnId': 2,
            'value': 'Some Value'
        })

        row2 = Row()
        row2.to_bottom = True
        row2.cells.append({
            'columnId': 3,
            'value': 'Some Value'
        })

        response = self.client.Sheets.add_rows_with_partial_success(1, [row1, row2])

        assert response.result[0].cells[0].value == 'Some Value'
        assert response.failed_items[0].error.error_code == 1036

    @clean_api_error
    def test_rows_serialization(self):
        pytest.skip('Skipping until mock API test is updated')
        self.client.as_test_scenario('Serialization - Rows')

        row = Row()
        row.expanded = True
        row.format_ = ',,,,,,,,4,,,,,,,'
        row.locked = False
        row.cells.append({
            'columnId': 2,
            'value': 'url link',
            'strict': False,
            'hyperlink': {
                'url': 'https://google.com'
            }
        })
        row.cells.append({
            'columnId': 3,
            'value': 'sheet id link',
            'strict': False,
            'hyperlink': {
                'sheetId': 4
            }
        })
        row.cells.append({
            'columnId': 5,
            'value': 'report id link',
            'strict': False,
            'hyperlink': {
                'reportId': 6
            }
        })

        response = self.client.Sheets.add_rows(1, row)

        cells = response.result.cells

        assert cells[0].hyperlink.url == 'https://google.com'
        assert cells[1].hyperlink.sheet_id == 4
        assert cells[2].hyperlink.report_id == 6

    @clean_api_error
    def test_cell_link_serialization(self):
        pytest.skip('Skipping until mock API test is updated')
        self.client.as_test_scenario('Serialization - Cell Link')

        updated_row = Row()
        updated_row.id = 2
        updated_row.cells.append({
            'columnId': 3,
            'value': ExplicitNull(),
            'linkInFromCell': {
                'sheetId': 4,
                'rowId': 5,
                'columnId': 6
            }
        })

        self.client.Sheets.update_rows(1, updated_row)

    @clean_api_error
    def test_favorite_serialization(self):
        pytest.skip('Skipping until mock API test is updated')
        self.client.as_test_scenario('Serialization - Favorite')

        response = self.client.Favorites.add_favorites(Favorite({
            'type': 'sheet',
            'objectId': 1
        }))

        assert response.result.type == 'sheet'

    @clean_api_error
    def test_report_serialization(self):
        self.client.as_test_scenario('Serialization - Report')

        report = self.client.Reports.get_report(1)

        assert report.effective_attachment_options[0] == 'GOOGLE_DRIVE'
        assert report.columns[0].virtual_id == 2
        assert report.rows[0].cells[0].virtual_column_id == 2

    @clean_api_error
    def test_share_serialization(self):
        pytest.skip('Skipping until mock API test is updated')
        self.client.as_test_scenario('Serialization - Share')

        share = Share({
            'email': 'john.doe@smartsheet.com',
            'accessLevel': 'VIEWER',
            'subject': 'Check out this sheet',
            'message': 'Let me know what you think. Thanks!',
            'ccMe': True
        })

        response = self.client.Sheets.share_sheet(1, share, send_email=True)

        assert response.result.id == 'abc'

    @clean_api_error
    def test_send_via_email_serialization(self):
        self.client.as_test_scenario('Serialization - Send via Email')

        response = self.client.Sheets.send_sheet(1, SheetEmail({
            'send_to': [
                Recipient({
                    'email': 'john.doe@smartsheet.com'
                }),
                Recipient({
                    'groupId': 2
                })
            ],
            'subject': 'Some subject',
            'message': 'Some message',
            'ccMe': True,
            'format': 'PDF',
            'formatDetails': FormatDetails({
                'paperSize': 'LETTER'
            })
        }))

        assert response.message == 'SUCCESS'

    @clean_api_error
    def test_row_email_serialization(self):
        self.client.as_test_scenario('Serialization - Row Email')

        response = self.client.Sheets.send_rows(1, MultiRowEmail({
            'send_to': [Recipient({
                'groupId': 2
            })],
            'subject': 'Some subject',
            'message': 'Some message',
            'includeAttachments': False,
            'includeDiscussions': True,
            'layout': 'VERTICAL',
            'rowIds': [
                4
            ],
            'columnIds': [
                3
            ]
        }))

        assert response.message == 'SUCCESS'

    @clean_api_error
    def test_template_serialization(self):
        self.client.as_test_scenario('Serialization - Template')

        templates = self.client.Templates.list_public_templates()

        assert templates.data[0].categories[0] == 'Featured Templates'

    @clean_api_error
    def test_update_request_serialization(self):
        pytest.skip('Date serialization is not easily configurable currently')

        self.client.as_test_scenario('Serialization - Update Request')

        update_request = UpdateRequest({
            'sendTo': [
                Recipient({
                    'email': 'john.doe@smartsheet.com'
                })
            ],
            'rowIds': [
                2
            ],
            'columnIds': [
                3
            ],
            'includeAttachments': True,
            'includeDiscussions': False,
            'subject': 'Some subject',
            'message': 'Some message',
            'ccMe': True,
            'schedule': Schedule({
                'type': 'MONTHLY',
                'startAt': '2018-03-01T19:00:00Z',
                'endAt': '2018-06-01T00:00:00Z',
                'dayOrdinal': 'FIRST',
                'dayDescriptors': [
                    'FRIDAY'
                ],
                'repeatEvery': 1
            })
        })

        response = self.client.Sheets.send_update_request(1, update_request)

        result = response.result

        assert result.send_to[0].email == 'john.doe@smartsheet.com'
        assert result.column_ids[0] == 3
        assert result.row_ids[0] == 2
        assert result.sent_by.name == 'Jane Doe'
        assert result.schedule.day_descriptors[0] == 'FRIDAY'

    @clean_api_error
    def test_sent_update_request_serialization(self):
        self.client.as_test_scenario('Serialization - Sent Update Requests')

        sent_update_request = self.client.Sheets.get_sent_update_request(1, 2)

        assert sent_update_request.sent_by.name == 'Jane Doe'
        assert sent_update_request.sent_to.email == 'john.doe@smartsheet.com'
        assert sent_update_request.row_ids[0] == 4
        assert sent_update_request.column_ids[0] == 5

    @clean_api_error
    def test_sheet_settings_serialization(self):
        pytest.skip('Date serialization is not easily configurable currently')

        self.client.as_test_scenario('Serialization - Sheet Settings')

        response = self.client.Sheets.update_sheet(1, Sheet({
            'userSettings': {
                'criticalPathEnabled': True,
                'displaySummaryTasks': True
            },
            'projectSettings': {
                'workingDays': [
                    'MONDAY',
                    'TUESDAY'
                ],
                'nonWorkingDays': [
                    '2018-04-04',
                    '2018-05-05',
                    '2018-06-06'
                ],
                'lengthOfDay': 23.5
            }
        }))

        result = response.result

        assert result.user_settings.critical_path_enabled
        assert result.project_settings.working_days[0] == 'MONDAY'
        assert result.project_settings.non_working_days[0] == '2018-04-04'

    @clean_api_error
    def test_container_destination_serialization(self):
        pytest.skip('Skipping until mock API test is updated')
        pytest.skip('Models currently have no concept of a nullable / optional type')

        self.client.as_test_scenario('Serialization - Container Destination')

        response = self.client.Folders.copy_folder(1, ContainerDestination({
            'destinationType': 'home',
            'destinationId': ExplicitNull(),
            'newName': 'Copy of Some Folder'
        }))

        assert response.result.id == 2

    @clean_api_error
    def test_cross_sheet_reference_serialization(self):
        self.client.as_test_scenario('Serialization - Cross Sheet Reference')

        response = self.client.Sheets.create_cross_sheet_reference(1, CrossSheetReference({
            'name': 'Some Cross Sheet Reference',
            'sourceSheetId': 2,
            'startRowId': 3,
            'endRowId': 4,
            'startColumnId': 5,
            'endColumnId': 6
        }))

        assert response.result.name == 'Some Cross Sheet Reference'
