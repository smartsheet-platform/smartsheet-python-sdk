import pytest
import smartsheet


# Given Python's variable naming convention of snake_case,
# and Smartsheet's API attribute naming convention of
# lowerCamelCase, this set of tests is intended to make
# sure all of that is handled correctly.

@pytest.mark.usefixtures("smart_setup")
class TestModelAttributes:
    def test_row(self, smart_setup):
        smart = smart_setup['smart']
        # above, above
        # access_level, accessLevel
        # attachments, attachments
        # cells, cells
        # columns, columns
        # conditional_format, conditionalFormat
        # created_at, createdAt
        # discussions, discussions
        # expanded, expanded
        # filtered_out, filteredOut
        # _format, format
        # _id, id
        # in_critical_path, inCriticalPath
        # locked, locked
        # locked_for_user, lockedForUser
        # modified_at, modifiedAt
        # parent_id, parentId
        # permalink, permalink
        # row_number, rowNumber
        # sheet_id, sheetId
        # sibling_id, siblingId
        # to_bottom, toBottom
        # to_top, toTop
        # version, version
        model = smart.models.Row({
            'above': True,
            'accessLevel': 'VIEWER',
            'attachments': smart.models.Attachment(),
            'cells': smart.models.Cell(),
            'columns': smart.models.Column(),
            'conditionalFormat': 'foo',
            'discussions': smart.models.Discussion(),
            'expanded': True,
            'filteredOut': True,
            'format': 'foo',
            'id': 19082,
            'inCriticalPath': True,
            'locked': True,
            'lockedForUser': True,
            'parentId': 19082,
            'permalink': 'foo',
            'rowNumber': 19082,
            'sheetId': 19082,
            'siblingId': 19082,
            'toBottom': True,
            'toTop': True,
            'version': 19082
        })

        assert model.above == True
        assert model.access_level == 'VIEWER'
        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert isinstance(model.cells[0], smart.models.Cell)
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.conditional_format == 'foo'
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model.expanded == True
        assert model.filtered_out == True
        assert model._format == 'foo'
        assert model._id == 19082
        assert model.in_critical_path == True
        assert model.locked == True
        assert model.locked_for_user == True
        assert model.parent_id == 19082
        assert model.permalink == 'foo'
        assert model.row_number == 19082
        assert model.sheet_id == 19082
        assert model.sibling_id == 19082
        assert model.to_bottom == True
        assert model.to_top == True
        assert model.version == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_row_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Row({
            'above': True,
            'attachments': smart.models.Attachment(),
            'cells': smart.models.Cell(),
            'columns': smart.models.Column(),
            'discussions': smart.models.Discussion(),
            'expanded': True,
            'filteredOut': True,
            'locked': True,
            'lockedForUser': True,
            'permalink': 'foo',
            'rowNumber': 19082,
            'sheetId': 19082,
            'version': 19082,
            'access_level': 'VIEWER',
            'conditional_format': 'foo',
            '_format': 'foo',
            '_id': 19082,
            'in_critical_path': True,
            'parent_id': 19082,
            'sibling_id': 19082,
            'to_bottom': True,
            'to_top': True
        })

        assert model.above == True
        assert model.access_level == 'VIEWER'
        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert isinstance(model.cells[0], smart.models.Cell)
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.conditional_format == 'foo'
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model.expanded == True
        assert model.filtered_out == True
        assert model._format == 'foo'
        assert model._id == 19082
        assert model.in_critical_path == True
        assert model.locked == True
        assert model.locked_for_user == True
        assert model.parent_id == 19082
        assert model.permalink == 'foo'
        assert model.row_number == 19082
        assert model.sheet_id == 19082
        assert model.sibling_id == 19082
        assert model.to_bottom == True
        assert model.to_top == True
        assert model.version == 19082

    def test_home(self, smart_setup):
        smart = smart_setup['smart']
        # folders, folders
        # reports, reports
        # sheets, sheets
        # templates, templates
        # workspaces, workspaces
        model = smart.models.Home({
            'folders': smart.models.Folder(),
            'reports': smart.models.Report(),
            'sheets': smart.models.Sheet(),
            'templates': smart.models.Template(),
            'workspaces': smart.models.Workspace()
        })

        assert isinstance(model.folders[0], smart.models.Folder)
        assert isinstance(model.reports[0], smart.models.Report)
        assert isinstance(model.sheets[0], smart.models.Sheet)
        assert isinstance(model.templates[0], smart.models.Template)
        assert isinstance(model.workspaces[0], smart.models.Workspace)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_cell(self, smart_setup):
        smart = smart_setup['smart']
        # column_id, columnId
        # column_type, columnType
        # conditional_format, conditionalFormat
        # display_value, displayValue
        # _format, format
        # formula, formula
        # hyperlink, hyperlink
        # link_in_from_cell, linkInFromCell
        # links_out_to_cells, linksOutToCells
        # strict, strict
        # value, value
        model = smart.models.Cell({
            'columnId': 19082,
            'columnType': 'foo',
            'conditionalFormat': 'foo',
            'displayValue': 'foo',
            'format': 'foo',
            'formula': 'foo',
            'hyperlink': smart.models.Hyperlink(),
            'linkInFromCell': smart.models.CellLink(),
            'linksOutToCells': smart.models.CellLink(),
            'strict': True,
            'value': 'foo'
        })

        assert model.column_id == 19082
        assert model.column_type == 'foo'
        assert model.conditional_format == 'foo'
        assert model.display_value == 'foo'
        assert model._format == 'foo'
        assert model.formula == 'foo'
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        assert model.strict == True
        assert model.value == 'foo'
        model.hyperlink = {}
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        model.linkInFromCell = {}
        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        model.linksOutToCells = {}
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_cell_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Cell({
            'columnType': 'foo',
            'conditionalFormat': 'foo',
            'displayValue': 'foo',
            'formula': 'foo',
            'hyperlink': smart.models.Hyperlink(),
            'strict': True,
            'value': 'foo',
            'column_id': 19082,
            '_format': 'foo',
            'link_in_from_cell': smart.models.CellLink(),
            'links_out_to_cells': smart.models.CellLink()
        })

        assert model.column_id == 19082
        assert model.column_type == 'foo'
        assert model.conditional_format == 'foo'
        assert model.display_value == 'foo'
        assert model._format == 'foo'
        assert model.formula == 'foo'
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        assert model.strict == True
        assert model.value == 'foo'

    def test_user(self, smart_setup):
        smart = smart_setup['smart']
        # admin, admin
        # email, email
        # first_name, firstName
        # group_admin, groupAdmin
        # _id, id
        # last_name, lastName
        # licensed_sheet_creator, licensedSheetCreator
        # name, name
        # resource_viewer, resourceViewer
        # status, status
        model = smart.models.User({
            'admin': True,
            'email': 'foo',
            'firstName': 'foo',
            'groupAdmin': True,
            'id': 19082,
            'lastName': 'foo',
            'licensedSheetCreator': True,
            'name': 'foo',
            'resourceViewer': True,
            'status': 'ACTIVE'
        })

        assert model.admin == True
        assert model.email == 'foo'
        assert model.first_name == 'foo'
        assert model.group_admin == True
        assert model._id == 19082
        assert model.last_name == 'foo'
        assert model.licensed_sheet_creator == True
        assert model.name == 'foo'
        assert model.resource_viewer == True
        assert model.status == 'ACTIVE'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_user_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.User({
            'admin': True,
            'email': 'foo',
            'name': 'foo',
            'status': 'ACTIVE',
            'first_name': 'foo',
            'group_admin': True,
            '_id': 19082,
            'last_name': 'foo',
            'licensed_sheet_creator': True,
            'resource_viewer': True
        })

        assert model.admin == True
        assert model.email == 'foo'
        assert model.first_name == 'foo'
        assert model.group_admin == True
        assert model._id == 19082
        assert model.last_name == 'foo'
        assert model.licensed_sheet_creator == True
        assert model.name == 'foo'
        assert model.resource_viewer == True
        assert model.status == 'ACTIVE'

    def test_group(self, smart_setup):
        smart = smart_setup['smart']
        # created_at, createdAt
        # description, description
        # _id, id
        # members, members
        # modified_at, modifiedAt
        # name, name
        # owner, owner
        # owner_id, ownerId
        model = smart.models.Group({
            'description': 'foo',
            'id': 19082,
            'members': smart.models.GroupMember(),
            'name': 'foo',
            'owner': 'foo',
            'ownerId': 19082
        })

        assert model.description == 'foo'
        assert model._id == 19082
        assert isinstance(model.members[0], smart.models.GroupMember)
        assert model.name == 'foo'
        assert model.owner == 'foo'
        assert model.owner_id == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_group_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Group({
            'description': 'foo',
            'id': 19082,
            'members': smart.models.GroupMember(),
            'name': 'foo',
            'owner': 'foo',
            'owner_id': 19082
        })

        assert model.description == 'foo'
        assert model._id == 19082
        assert isinstance(model.members[0], smart.models.GroupMember)
        assert model.name == 'foo'
        assert model.owner == 'foo'
        assert model.owner_id == 19082

    def test_error(self, smart_setup):
        smart = smart_setup['smart']
        # request_response, requestResponse
        # result, result
        model = smart.models.Error({
            'result': smart.models.ErrorResult()
        })

        assert isinstance(model.result, smart.models.ErrorResult)
        model.result = {}
        assert isinstance(model.result, smart.models.ErrorResult)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_error_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Error({
            'result': smart.models.ErrorResult()
        })

        assert isinstance(model.result, smart.models.ErrorResult)

    def test_email(self, smart_setup):
        smart = smart_setup['smart']
        # cc_me, ccMe
        # message, message
        # send_to, sendTo
        # subject, subject
        model = smart.models.Email({
            'ccMe': True,
            'message': 'foo',
            'sendTo': smart.models.Recipient(),
            'subject': 'foo'
        })

        assert model.cc_me == True
        assert model.message == 'foo'
        assert isinstance(model.send_to[0], smart.models.Recipient)
        assert model.subject == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_email_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Email({
            'message': 'foo',
            'subject': 'foo',
            'cc_me': True,
            'send_to': smart.models.Recipient()
        })

        assert model.cc_me == True
        assert model.message == 'foo'
        assert isinstance(model.send_to[0], smart.models.Recipient)
        assert model.subject == 'foo'

    def test_sheet(self, smart_setup):
        smart = smart_setup['smart']
        # access_level, accessLevel
        # attachments, attachments
        # columns, columns
        # created_at, createdAt
        # dependencies_enabled, dependenciesEnabled
        # discussions, discussions
        # effective_attachment_options, effectiveAttachmentOptions
        # favorite, favorite
        # from_id, fromId
        # gantt_enabled, ganttEnabled
        # _id, id
        # modified_at, modifiedAt
        # name, name
        # owner, owner
        # owner_id, ownerId
        # permalink, permalink
        # read_only, readOnly
        # resource_management_enabled, resourceManagementEnabled
        # rows, rows
        # show_parent_rows_for_filters, showParentRowsForFilters
        # source, source
        # total_row_count, totalRowCount
        # user_settings, userSettings
        # version, version
        model = smart.models.Sheet({
            'accessLevel': 'VIEWER',
            'attachments': smart.models.Attachment(),
            'columns': smart.models.Column(),
            'dependenciesEnabled': True,
            'discussions': smart.models.Discussion(),
            'effectiveAttachmentOptions': ['foo'],
            'favorite': True,
            'fromId': 19082,
            'ganttEnabled': True,
            'id': 19082,
            'name': 'foo',
            'owner': 'foo',
            'ownerId': 19082,
            'permalink': 'foo',
            'readOnly': True,
            'resourceManagementEnabled': True,
            'rows': smart.models.Row(),
            'showParentRowsForFilters': True,
            'source': smart.models.Source(),
            'totalRowCount': 19082,
            'userSettings': smart.models.SheetUserSettings(),
            'version': 19082
        })

        assert model.access_level == 'VIEWER'
        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.dependencies_enabled == True
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model.effective_attachment_options[0] == 'foo'
        assert model.favorite == True
        assert model.from_id == 19082
        assert model.gantt_enabled == True
        assert model._id == 19082
        assert model.name == 'foo'
        assert model.owner == 'foo'
        assert model.owner_id == 19082
        assert model.permalink == 'foo'
        assert model.read_only == True
        assert model.resource_management_enabled == True
        assert isinstance(model.rows[0], smart.models.Row)
        assert model.show_parent_rows_for_filters == True
        assert isinstance(model.source, smart.models.Source)
        assert model.total_row_count == 19082
        assert isinstance(model.user_settings, smart.models.SheetUserSettings)
        assert model.version == 19082
        model.effective_attachment_options = 'foo'
        assert model.effective_attachment_options[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.effective_attachment_options = tmplist
        assert model.effective_attachment_options[0] == 'foo'
        model.source = {}
        assert isinstance(model.source, smart.models.Source)
        model.userSettings = {}
        assert isinstance(model.user_settings, smart.models.SheetUserSettings)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_sheet_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Sheet({
            'attachments': smart.models.Attachment(),
            'columns': smart.models.Column(),
            'discussions': smart.models.Discussion(),
            'favorite': True,
            'name': 'foo',
            'owner': 'foo',
            'permalink': 'foo',
            'rows': smart.models.Row(),
            'source': smart.models.Source(),
            'version': 19082,
            'access_level': 'VIEWER',
            'dependencies_enabled': True,
            'effective_attachment_options': ['foo'],
            'from_id': 19082,
            'gantt_enabled': True,
            '_id': 19082,
            'owner_id': 19082,
            'read_only': True,
            'resource_management_enabled': True,
            'show_parent_rows_for_filters': True,
            'total_row_count': 19082,
            'user_settings': smart.models.SheetUserSettings()
        })

        assert model.access_level == 'VIEWER'
        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.dependencies_enabled == True
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model.effective_attachment_options[0] == 'foo'
        assert model.favorite == True
        assert model.from_id == 19082
        assert model.gantt_enabled == True
        assert model._id == 19082
        assert model.name == 'foo'
        assert model.owner == 'foo'
        assert model.owner_id == 19082
        assert model.permalink == 'foo'
        assert model.read_only == True
        assert model.resource_management_enabled == True
        assert isinstance(model.rows[0], smart.models.Row)
        assert model.show_parent_rows_for_filters == True
        assert isinstance(model.source, smart.models.Source)
        assert model.total_row_count == 19082
        assert isinstance(model.user_settings, smart.models.SheetUserSettings)
        assert model.version == 19082

    def test_share(self, smart_setup):
        smart = smart_setup['smart']
        # access_level, accessLevel
        # cc_me, ccMe
        # email, email
        # group_id, groupId
        # _id, id
        # message, message
        # name, name
        # subject, subject
        # _type, type
        # user_id, userId
        model = smart.models.Share({
            'accessLevel': 'VIEWER',
            'ccMe': True,
            'email': 'foo',
            'groupId': 19082,
            'id': 'foo',
            'message': 'foo',
            'name': 'foo',
            'subject': 'foo',
            'type': 'USER',
            'userId': 19082
        })

        assert model.access_level == 'VIEWER'
        assert model.cc_me == True
        assert model.email == 'foo'
        assert model.group_id == 19082
        assert model._id == 'foo'
        assert model.message == 'foo'
        assert model.name == 'foo'
        assert model.subject == 'foo'
        assert model._type == 'USER'
        assert model.user_id == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_share_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Share({
            'email': 'foo',
            'message': 'foo',
            'name': 'foo',
            'subject': 'foo',
            'access_level': 'VIEWER',
            'cc_me': True,
            'group_id': 19082,
            '_id': 'foo',
            '_type': 'USER',
            'user_id': 19082
        })

        assert model.access_level == 'VIEWER'
        assert model.cc_me == True
        assert model.email == 'foo'
        assert model.group_id == 19082
        assert model._id == 'foo'
        assert model.message == 'foo'
        assert model.name == 'foo'
        assert model.subject == 'foo'
        assert model._type == 'USER'
        assert model.user_id == 19082

    def test_source(self, smart_setup):
        smart = smart_setup['smart']
        # _id, id
        # _type, type
        model = smart.models.Source({
            'id': 19082,
            'type': 'sheet'
        })

        assert model._id == 19082
        assert model._type == 'sheet'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_source_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Source({
            'id': 19082,
            'type': 'sheet'
        })

        assert model._id == 19082
        assert model._type == 'sheet'

    def test_report(self, smart_setup):
        smart = smart_setup['smart']
        # source_sheets, sourceSheets
        # from_id, fromId
        # modified_at, modifiedAt
        # owner_id, ownerId
        # columns, columns
        # dependencies_enabled, dependenciesEnabled
        # discussions, discussions
        # version, version
        # _id, id
        # gantt_enabled, ganttEnabled
        # show_parent_rows_for_filters, showParentRowsForFilters
        # created_at, createdAt
        # name, name
        # attachments, attachments
        # total_row_count, totalRowCount
        # favorite, favorite
        # access_level, accessLevel
        # rows, rows
        # read_only, readOnly
        # permalink, permalink
        # source, source
        # effective_attachment_options, effectiveAttachmentOptions
        # owner, owner
        # resource_management_enabled, resourceManagementEnabled
        # user_settings, userSettings
        model = smart.models.Report({
            'sourceSheets': smart.models.Sheet(),
            'fromId': 19082,
            'ownerId': 19082,
            'columns': smart.models.Column(),
            'dependenciesEnabled': True,
            'discussions': smart.models.Discussion(),
            'version': 19082,
            'id': 19082,
            'ganttEnabled': True,
            'showParentRowsForFilters': True,
            'name': 'foo',
            'attachments': smart.models.Attachment(),
            'totalRowCount': 19082,
            'favorite': True,
            'accessLevel': 'VIEWER',
            'rows': smart.models.Row(),
            'readOnly': True,
            'permalink': 'foo',
            'source': smart.models.Source(),
            'effectiveAttachmentOptions': ['foo'],
            'owner': 'foo',
            'resourceManagementEnabled': True,
            'userSettings': smart.models.SheetUserSettings()
        })

        assert isinstance(model.source_sheets[0], smart.models.Sheet)
        assert model.from_id == 19082
        assert model.owner_id == 19082
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.dependencies_enabled == True
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model.version == 19082
        assert model._id == 19082
        assert model.gantt_enabled == True
        assert model.show_parent_rows_for_filters == True
        assert model.name == 'foo'
        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert model.total_row_count == 19082
        assert model.favorite == True
        assert model.access_level == 'VIEWER'
        assert isinstance(model.rows[0], smart.models.Row)
        assert model.read_only == True
        assert model.permalink == 'foo'
        assert isinstance(model.source, smart.models.Source)
        assert model.effective_attachment_options[0] == 'foo'
        assert model.owner == 'foo'
        assert model.resource_management_enabled == True
        assert isinstance(model.user_settings, smart.models.SheetUserSettings)
        model.source = {}
        assert isinstance(model.source, smart.models.Source)
        model.effective_attachment_options = 'foo'
        assert model.effective_attachment_options[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.effective_attachment_options = tmplist
        assert model.effective_attachment_options[0] == 'foo'
        model.userSettings = {}
        assert isinstance(model.user_settings, smart.models.SheetUserSettings)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_report_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Report({
            'columns': smart.models.Column(),
            'discussions': smart.models.Discussion(),
            'version': 19082,
            'name': 'foo',
            'attachments': smart.models.Attachment(),
            'favorite': True,
            'rows': smart.models.Row(),
            'permalink': 'foo',
            'source': smart.models.Source(),
            'owner': 'foo',
            'source_sheets': smart.models.Sheet(),
            'from_id': 19082,
            'owner_id': 19082,
            'dependencies_enabled': True,
            '_id': 19082,
            'gantt_enabled': True,
            'show_parent_rows_for_filters': True,
            'total_row_count': 19082,
            'access_level': 'VIEWER',
            'read_only': True,
            'effective_attachment_options': ['foo'],
            'resource_management_enabled': True,
            'user_settings': smart.models.SheetUserSettings()
        })

        assert isinstance(model.source_sheets[0], smart.models.Sheet)
        assert model.from_id == 19082
        assert model.owner_id == 19082
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.dependencies_enabled == True
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model.version == 19082
        assert model._id == 19082
        assert model.gantt_enabled == True
        assert model.show_parent_rows_for_filters == True
        assert model.name == 'foo'
        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert model.total_row_count == 19082
        assert model.favorite == True
        assert model.access_level == 'VIEWER'
        assert isinstance(model.rows[0], smart.models.Row)
        assert model.read_only == True
        assert model.permalink == 'foo'
        assert isinstance(model.source, smart.models.Source)
        assert model.effective_attachment_options[0] == 'foo'
        assert model.owner == 'foo'
        assert model.resource_management_enabled == True
        assert isinstance(model.user_settings, smart.models.SheetUserSettings)

    def test__filter(self, smart_setup):
        smart = smart_setup['smart']
        # criteria, criteria
        # exclude_selected, excludeSelected
        # _type, type
        # values, values
        model = smart.models.Filter({
            'criteria': smart.models.Criteria(),
            'excludeSelected': True,
            'type': 'LIST',
            'values': ['foo']
        })

        assert isinstance(model.criteria[0], smart.models.Criteria)
        assert model.exclude_selected == True
        assert model._type == 'LIST'
        assert model.values[0] == 'foo'
        model.values = 'foo'
        assert model.values[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.values = tmplist
        assert model.values[0] == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test__filter_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Filter({
            'criteria': smart.models.Criteria(),
            'values': ['foo'],
            'exclude_selected': True,
            '_type': 'LIST'
        })

        assert isinstance(model.criteria[0], smart.models.Criteria)
        assert model.exclude_selected == True
        assert model._type == 'LIST'
        assert model.values[0] == 'foo'

    def test_folder(self, smart_setup):
        smart = smart_setup['smart']
        # favorite, favorite
        # folders, folders
        # _id, id
        # name, name
        # permalink, permalink
        # reports, reports
        # sheets, sheets
        # templates, templates
        model = smart.models.Folder({
            'favorite': True,
            'folders': smart.models.Folder(),
            'id': 19082,
            'name': 'foo',
            'permalink': 'foo',
            'reports': smart.models.Report(),
            'sheets': smart.models.Sheet(),
            'templates': smart.models.Template()
        })

        assert model.favorite == True
        assert isinstance(model.folders[0], smart.models.Folder)
        assert model._id == 19082
        assert model.name == 'foo'
        assert model.permalink == 'foo'
        assert isinstance(model.reports[0], smart.models.Report)
        assert isinstance(model.sheets[0], smart.models.Sheet)
        assert isinstance(model.templates[0], smart.models.Template)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_folder_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Folder({
            'favorite': True,
            'folders': smart.models.Folder(),
            'name': 'foo',
            'permalink': 'foo',
            'reports': smart.models.Report(),
            'sheets': smart.models.Sheet(),
            'templates': smart.models.Template(),
            '_id': 19082
        })

        assert model.favorite == True
        assert isinstance(model.folders[0], smart.models.Folder)
        assert model._id == 19082
        assert model.name == 'foo'
        assert model.permalink == 'foo'
        assert isinstance(model.reports[0], smart.models.Report)
        assert isinstance(model.sheets[0], smart.models.Sheet)
        assert isinstance(model.templates[0], smart.models.Template)

    def test_column(self, smart_setup):
        smart = smart_setup['smart']
        # auto_number_format, autoNumberFormat
        # _filter, filter
        # _format, format
        # hidden, hidden
        # _id, id
        # index, index
        # locked, locked
        # locked_for_user, lockedForUser
        # options, options
        # primary, primary
        # symbol, symbol
        # system_column_type, systemColumnType
        # tags, tags
        # title, title
        # _type, type
        # width, width
        model = smart.models.Column({
            'autoNumberFormat': smart.models.AutoNumberFormat(),
            'filter': smart.models.Filter(),
            'format': 'foo',
            'hidden': True,
            'id': 19082,
            'index': 19082,
            'locked': True,
            'lockedForUser': True,
            'options': ['foo'],
            'primary': True,
            'symbol': 'STAR',
            'systemColumnType': 'AUTO_NUMBER',
            'tags': ['foo'],
            'title': 'foo',
            'type': 'TEXT_NUMBER',
            'width': 19082
        })

        assert isinstance(model.auto_number_format, smart.models.AutoNumberFormat)
        assert isinstance(model._filter, smart.models.Filter)
        assert model._format == 'foo'
        assert model.hidden == True
        assert model._id == 19082
        assert model.index == 19082
        assert model.locked == True
        assert model.locked_for_user == True
        assert model.options[0] == 'foo'
        assert model.primary == True
        assert model.symbol == 'STAR'
        assert model.system_column_type == 'AUTO_NUMBER'
        assert model.tags[0] == 'foo'
        assert model.title == 'foo'
        assert model._type == 'TEXT_NUMBER'
        assert model.width == 19082
        model.autoNumberFormat = {}
        assert isinstance(model.auto_number_format, smart.models.AutoNumberFormat)
        model.filter = {}
        assert isinstance(model._filter, smart.models.Filter)
        model.options = 'foo'
        assert model.options[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.options = tmplist
        assert model.options[0] == 'foo'
        model.tags = 'foo'
        assert model.tags[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.tags = tmplist
        assert model.tags[0] == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_column_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Column({
            'hidden': True,
            'index': 19082,
            'locked': True,
            'options': ['foo'],
            'primary': True,
            'symbol': 'STAR',
            'tags': ['foo'],
            'title': 'foo',
            'width': 19082,
            'auto_number_format': smart.models.AutoNumberFormat(),
            '_filter': smart.models.Filter(),
            '_format': 'foo',
            '_id': 19082,
            'locked_for_user': True,
            'system_column_type': 'AUTO_NUMBER',
            '_type': 'TEXT_NUMBER'
        })

        assert isinstance(model.auto_number_format, smart.models.AutoNumberFormat)
        assert isinstance(model._filter, smart.models.Filter)
        assert model._format == 'foo'
        assert model.hidden == True
        assert model._id == 19082
        assert model.index == 19082
        assert model.locked == True
        assert model.locked_for_user == True
        assert model.options[0] == 'foo'
        assert model.primary == True
        assert model.symbol == 'STAR'
        assert model.system_column_type == 'AUTO_NUMBER'
        assert model.tags[0] == 'foo'
        assert model.title == 'foo'
        assert model._type == 'TEXT_NUMBER'
        assert model.width == 19082

    def test_result(self, smart_setup):
        smart = smart_setup['smart']
        # message, message
        # result, result
        # result_code, resultCode
        # version, version
        model = smart.models.Result({
            'message': 'foo',
            'resultCode': 19082,
            'version': 19082
        })

        assert model.message == 'foo'
        assert model.result_code == 19082
        assert model.version == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_result_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Result({
            'message': 'foo',
            'version': 19082,
            'result_code': 19082
        })

        assert model.message == 'foo'
        assert model.result_code == 19082
        assert model.version == 19082

    def test_contact(self, smart_setup):
        smart = smart_setup['smart']
        # email, email
        # _id, id
        # name, name
        model = smart.models.Contact({
            'email': 'foo',
            'id': 'foo',
            'name': 'foo'
        })

        assert model.email == 'foo'
        assert model._id == 'foo'
        assert model.name == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_contact_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Contact({
            'email': 'foo',
            'name': 'foo',
            '_id': 'foo'
        })

        assert model.email == 'foo'
        assert model._id == 'foo'
        assert model.name == 'foo'

    def test_comment(self, smart_setup):
        smart = smart_setup['smart']
        # attachments, attachments
        # created_at, createdAt
        # created_by, createdBy
        # discussion_id, discussionId
        # _id, id
        # modified_at, modifiedAt
        # text, text
        model = smart.models.Comment({
            'attachments': smart.models.Attachment(),
            'createdBy': smart.models.User(),
            'discussionId': 19082,
            'id': 19082,
            'text': 'foo'
        })

        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert isinstance(model.created_by, smart.models.User)
        assert model.discussion_id == 19082
        assert model._id == 19082
        assert model.text == 'foo'
        model.createdBy = {}
        assert isinstance(model.created_by, smart.models.User)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_comment_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Comment({
            'attachments': smart.models.Attachment(),
            'text': 'foo',
            'created_by': smart.models.User(),
            'discussion_id': 19082,
            '_id': 19082
        })

        assert isinstance(model.attachments[0], smart.models.Attachment)
        assert isinstance(model.created_by, smart.models.User)
        assert model.discussion_id == 19082
        assert model._id == 19082
        assert model.text == 'foo'

    def test_account(self, smart_setup):
        smart = smart_setup['smart']
        # _id, id
        # name, name
        model = smart.models.Account({
            'id': 19082,
            'name': 'foo'
        })

        assert model._id == 19082
        assert model.name == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_account_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Account({
            'name': 'foo',
            '_id': 19082
        })

        assert model._id == 19082
        assert model.name == 'foo'

    def test_version(self, smart_setup):
        smart = smart_setup['smart']
        # version, version
        model = smart.models.Version({
            'version': 19082
        })

        assert model.version == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_cell_link(self, smart_setup):
        smart = smart_setup['smart']
        # column_id, columnId
        # row_id, rowId
        # sheet_id, sheetId
        # sheet_name, sheetName
        # status, status
        model = smart.models.CellLink({
            'columnId': 19082,
            'rowId': 19082,
            'sheetId': 19082,
            'sheetName': 'foo',
            'status': 'OK'
        })

        assert model.column_id == 19082
        assert model.row_id == 19082
        assert model.sheet_id == 19082
        assert model.sheet_name == 'foo'
        assert model.status == 'OK'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_cell_link_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.CellLink({
            'status': 'OK',
            'column_id': 19082,
            'row_id': 19082,
            'sheet_id': 19082,
            'sheet_name': 'foo'
        })

        assert model.column_id == 19082
        assert model.row_id == 19082
        assert model.sheet_id == 19082
        assert model.sheet_name == 'foo'
        assert model.status == 'OK'

    def test_template(self, smart_setup):
        smart = smart_setup['smart']
        # access_level, accessLevel
        # description, description
        # _id, id
        # name, name
        model = smart.models.Template({
            'accessLevel': 'VIEWER',
            'description': 'foo',
            'id': 19082,
            'name': 'foo'
        })

        assert model.access_level == 'VIEWER'
        assert model.description == 'foo'
        assert model._id == 19082
        assert model.name == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_template_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Template({
            'description': 'foo',
            'name': 'foo',
            'access_level': 'VIEWER',
            '_id': 19082
        })

        assert model.access_level == 'VIEWER'
        assert model.description == 'foo'
        assert model._id == 19082
        assert model.name == 'foo'

    def test_row_email(self, smart_setup):
        smart = smart_setup['smart']
        # message, message
        # column_ids, columnIds
        # send_to, sendTo
        # include_attachments, includeAttachments
        # subject, subject
        # include_discussions, includeDiscussions
        # cc_me, ccMe
        model = smart.models.RowEmail({
            'message': 'foo',
            'columnIds': [19082],
            'sendTo': smart.models.Recipient(),
            'includeAttachments': True,
            'subject': 'foo',
            'includeDiscussions': True,
            'ccMe': True
        })

        assert model.message == 'foo'
        assert model.column_ids[0] == 19082
        assert isinstance(model.send_to[0], smart.models.Recipient)
        assert model.include_attachments == True
        assert model.subject == 'foo'
        assert model.include_discussions == True
        assert model.cc_me == True
        model.column_ids = 19082
        assert model.column_ids[0] == 19082
        tmplist = smartsheet.types.TypedList(int)
        tmplist.append(19082)
        model.column_ids = tmplist
        assert model.column_ids[0] == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_row_email_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.RowEmail({
            'message': 'foo',
            'subject': 'foo',
            'column_ids': [19082],
            'send_to': smart.models.Recipient(),
            'include_attachments': True,
            'include_discussions': True,
            'cc_me': True
        })

        assert model.message == 'foo'
        assert model.column_ids[0] == 19082
        assert isinstance(model.send_to[0], smart.models.Recipient)
        assert model.include_attachments == True
        assert model.subject == 'foo'
        assert model.include_discussions == True
        assert model.cc_me == True

    def test_criteria(self, smart_setup):
        smart = smart_setup['smart']
        # operator, operator
        # value1, value1
        # value2, value2
        model = smart.models.Criteria({
            'operator': 'EQUAL',
            'value1': 'foo',
            'value2': 'foo'
        })

        assert model.operator == 'EQUAL'
        assert model.value1 == 'foo'
        assert model.value2 == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_currency(self, smart_setup):
        smart = smart_setup['smart']
        # code, code
        # symbol, symbol
        model = smart.models.Currency({
            'code': 'none',
            'symbol': 'foo'
        })

        assert model.code == 'none'
        assert model.symbol == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_favorite(self, smart_setup):
        smart = smart_setup['smart']
        # object_id, objectId
        # _type, type
        model = smart.models.Favorite({
            'objectId': 19082,
            'type': 'workspace'
        })

        assert model.object_id == 19082
        assert model._type == 'workspace'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_favorite_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Favorite({
            'object_id': 19082,
            '_type': 'workspace'
        })

        assert model.object_id == 19082
        assert model._type == 'workspace'

    def test_hyperlink(self, smart_setup):
        smart = smart_setup['smart']
        # report_id, reportId
        # sheet_id, sheetId
        # url, url
        model = smart.models.Hyperlink({
            'reportId': 19082,
            'sheetId': 19082,
            'url': 'foo'
        })

        assert model.report_id == 19082
        assert model.sheet_id == 19082
        assert model.url == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_hyperlink_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Hyperlink({
            'url': 'foo',
            'report_id': 19082,
            'sheet_id': 19082
        })

        assert model.report_id == 19082
        assert model.sheet_id == 19082
        assert model.url == 'foo'

    def test_recipient(self, smart_setup):
        smart = smart_setup['smart']
        # email, email
        # group_id, groupId
        model = smart.models.Recipient({
            'email': 'foo',
            'groupId': 19082
        })

        assert model.email == 'foo'
        assert model.group_id == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_recipient_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Recipient({
            'email': 'foo',
            'group_id': 19082
        })

        assert model.email == 'foo'
        assert model.group_id == 19082

    def test_workspace(self, smart_setup):
        smart = smart_setup['smart']
        # access_level, accessLevel
        # favorite, favorite
        # folders, folders
        # _id, id
        # name, name
        # permalink, permalink
        # reports, reports
        # sheets, sheets
        # templates, templates
        model = smart.models.Workspace({
            'accessLevel': 'VIEWER',
            'favorite': True,
            'folders': smart.models.Folder(),
            'id': 19082,
            'name': 'foo',
            'permalink': 'foo',
            'reports': smart.models.Report(),
            'sheets': smart.models.Sheet(),
            'templates': smart.models.Template()
        })

        assert model.access_level == 'VIEWER'
        assert model.favorite == True
        assert isinstance(model.folders[0], smart.models.Folder)
        assert model._id == 19082
        assert model.name == 'foo'
        assert model.permalink == 'foo'
        assert isinstance(model.reports[0], smart.models.Report)
        assert isinstance(model.sheets[0], smart.models.Sheet)
        assert isinstance(model.templates[0], smart.models.Template)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_workspace_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Workspace({
            'favorite': True,
            'folders': smart.models.Folder(),
            'name': 'foo',
            'permalink': 'foo',
            'reports': smart.models.Report(),
            'sheets': smart.models.Sheet(),
            'templates': smart.models.Template(),
            'access_level': 'VIEWER',
            '_id': 19082
        })

        assert model.access_level == 'VIEWER'
        assert model.favorite == True
        assert isinstance(model.folders[0], smart.models.Folder)
        assert model._id == 19082
        assert model.name == 'foo'
        assert model.permalink == 'foo'
        assert isinstance(model.reports[0], smart.models.Report)
        assert isinstance(model.sheets[0], smart.models.Sheet)
        assert isinstance(model.templates[0], smart.models.Template)

    def test_report_row(self, smart_setup):
        smart = smart_setup['smart']
        # in_critical_path, inCriticalPath
        # cells, cells
        # sibling_id, siblingId
        # modified_at, modifiedAt
        # columns, columns
        # row_number, rowNumber
        # _format, format
        # expanded, expanded
        # access_level, accessLevel
        # version, version
        # discussions, discussions
        # _id, id
        # parent_id, parentId
        # sheet_id, sheetId
        # to_top, toTop
        # to_bottom, toBottom
        # permalink, permalink
        # locked_for_user, lockedForUser
        # created_at, createdAt
        # conditional_format, conditionalFormat
        # filtered_out, filteredOut
        # above, above
        # locked, locked
        # attachments, attachments
        model = smart.models.ReportRow({
            'inCriticalPath': True,
            'cells': smart.models.Cell(),
            'siblingId': 19082,
            'columns': smart.models.Column(),
            'rowNumber': 19082,
            'format': 'foo',
            'expanded': True,
            'accessLevel': 'VIEWER',
            'version': 19082,
            'discussions': smart.models.Discussion(),
            'id': 19082,
            'parentId': 19082,
            'sheetId': 19082,
            'toTop': True,
            'toBottom': True,
            'permalink': 'foo',
            'lockedForUser': True,
            'conditionalFormat': 'foo',
            'filteredOut': True,
            'above': True,
            'locked': True,
            'attachments': smart.models.Attachment()
        })

        assert model.in_critical_path == True
        assert isinstance(model.cells[0], smart.models.Cell)
        assert model.sibling_id == 19082
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.row_number == 19082
        assert model._format == 'foo'
        assert model.expanded == True
        assert model.access_level == 'VIEWER'
        assert model.version == 19082
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model._id == 19082
        assert model.parent_id == 19082
        assert model.sheet_id == 19082
        assert model.to_top == True
        assert model.to_bottom == True
        assert model.permalink == 'foo'
        assert model.locked_for_user == True
        assert model.conditional_format == 'foo'
        assert model.filtered_out == True
        assert model.above == True
        assert model.locked == True
        assert isinstance(model.attachments[0], smart.models.Attachment)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_report_row_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.ReportRow({
            'cells': smart.models.Cell(),
            'columns': smart.models.Column(),
            'rowNumber': 19082,
            'expanded': True,
            'version': 19082,
            'discussions': smart.models.Discussion(),
            'permalink': 'foo',
            'lockedForUser': True,
            'filteredOut': True,
            'above': True,
            'locked': True,
            'attachments': smart.models.Attachment(),
            'in_critical_path': True,
            'sibling_id': 19082,
            '_format': 'foo',
            'access_level': 'VIEWER',
            '_id': 19082,
            'parent_id': 19082,
            'sheet_id': 19082,
            'to_top': True,
            'to_bottom': True,
            'conditional_format': 'foo'
        })

        assert model.in_critical_path == True
        assert isinstance(model.cells[0], smart.models.Cell)
        assert model.sibling_id == 19082
        assert isinstance(model.columns[0], smart.models.Column)
        assert model.row_number == 19082
        assert model._format == 'foo'
        assert model.expanded == True
        assert model.access_level == 'VIEWER'
        assert model.version == 19082
        assert isinstance(model.discussions[0], smart.models.Discussion)
        assert model._id == 19082
        assert model.parent_id == 19082
        assert model.sheet_id == 19082
        assert model.to_top == True
        assert model.to_bottom == True
        assert model.permalink == 'foo'
        assert model.locked_for_user == True
        assert model.conditional_format == 'foo'
        assert model.filtered_out == True
        assert model.above == True
        assert model.locked == True
        assert isinstance(model.attachments[0], smart.models.Attachment)

    def test_font_family(self, smart_setup):
        smart = smart_setup['smart']
        # name, name
        # traits, traits
        model = smart.models.FontFamily({
            'name': 'foo',
            'traits': ['foo']
        })

        assert model.name == 'foo'
        assert model.traits[0] == 'foo'
        model.traits = 'foo'
        assert model.traits[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.traits = tmplist
        assert model.traits[0] == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_server_info(self, smart_setup):
        smart = smart_setup['smart']
        # formats, formats
        # supported_locales, supportedLocales
        model = smart.models.ServerInfo({
            'formats': smart.models.FormatTables(),
            'supportedLocales': ['foo']
        })

        assert isinstance(model.formats, smart.models.FormatTables)
        assert model.supported_locales[0] == 'foo'
        model.formats = {}
        assert isinstance(model.formats, smart.models.FormatTables)
        model.supported_locales = 'foo'
        assert model.supported_locales[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.supported_locales = tmplist
        assert model.supported_locales[0] == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_server_info_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.ServerInfo({
            'formats': smart.models.FormatTables(),
            'supported_locales': ['foo']
        })

        assert isinstance(model.formats, smart.models.FormatTables)
        assert model.supported_locales[0] == 'foo'

    def test_report_cell(self, smart_setup):
        smart = smart_setup['smart']
        # link_in_from_cell, linkInFromCell
        # virtual_column_id, virtualColumnId
        # column_type, columnType
        # hyperlink, hyperlink
        # conditional_format, conditionalFormat
        # value, value
        # column_id, columnId
        # _format, format
        # strict, strict
        # display_value, displayValue
        # links_out_to_cells, linksOutToCells
        # formula, formula
        model = smart.models.ReportCell({
            'linkInFromCell': smart.models.CellLink(),
            'virtualColumnId': 19082,
            'columnType': 'foo',
            'hyperlink': smart.models.Hyperlink(),
            'conditionalFormat': 'foo',
            'value': 'foo',
            'columnId': 19082,
            'format': 'foo',
            'strict': True,
            'displayValue': 'foo',
            'linksOutToCells': smart.models.CellLink(),
            'formula': 'foo'
        })

        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        assert model.virtual_column_id == 19082
        assert model.column_type == 'foo'
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        assert model.conditional_format == 'foo'
        assert model.value == 'foo'
        assert model.column_id == 19082
        assert model._format == 'foo'
        assert model.strict == True
        assert model.display_value == 'foo'
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        assert model.formula == 'foo'
        model.linkInFromCell = {}
        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        model.hyperlink = {}
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        model.linksOutToCells = {}
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_report_cell_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.ReportCell({
            'columnType': 'foo',
            'hyperlink': smart.models.Hyperlink(),
            'conditionalFormat': 'foo',
            'value': 'foo',
            'strict': True,
            'displayValue': 'foo',
            'formula': 'foo',
            'link_in_from_cell': smart.models.CellLink(),
            'virtual_column_id': 19082,
            'column_id': 19082,
            '_format': 'foo',
            'links_out_to_cells': smart.models.CellLink()
        })

        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        assert model.virtual_column_id == 19082
        assert model.column_type == 'foo'
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        assert model.conditional_format == 'foo'
        assert model.value == 'foo'
        assert model.column_id == 19082
        assert model._format == 'foo'
        assert model.strict == True
        assert model.display_value == 'foo'
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        assert model.formula == 'foo'

    def test_row_mapping(self, smart_setup):
        smart = smart_setup['smart']
        # _from, from
        # to, to
        model = smart.models.RowMapping({
            'from': 19082,
            'to': 19082
        })

        assert model._from == 19082
        assert model.to == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_row_mapping_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.RowMapping({
            'to': 19082,
            '_from': 19082
        })

        assert model._from == 19082
        assert model.to == 19082

    def test_o_auth_error(self, smart_setup):
        smart = smart_setup['smart']
        # error, error
        # error_code, errorCode
        # error_description, error_description
        model = smart.models.OAuthError({
            'error': 'invalid_request',
            'errorCode': 19082,
            'error_description': 'foo'
        })

        assert model.error == 'invalid_request'
        assert model.error_code == 19082
        assert model.error_description == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_o_auth_error_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.OAuthError({
            'error': 'invalid_request',
            'error_description': 'foo',
            'error_code': 19082
        })

        assert model.error == 'invalid_request'
        assert model.error_code == 19082
        assert model.error_description == 'foo'

    def test_discussion(self, smart_setup):
        smart = smart_setup['smart']
        # access_level, accessLevel
        # comment, comment
        # comment_attachments, commentAttachments
        # comments, comments
        # created_by, createdBy
        # _id, id
        # last_commented_at, lastCommentedAt
        # last_commented_user, lastCommentedUser
        # parent_id, parentId
        # parent_type, parentType
        # read_only, readOnly
        # title, title
        model = smart.models.Discussion({
            'accessLevel': 'VIEWER',
            'comment': smart.models.Comment(),
            'commentAttachments': smart.models.Attachment(),
            'comments': smart.models.Comment(),
            'createdBy': smart.models.User(),
            'id': 19082,
            'lastCommentedUser': smart.models.User(),
            'parentId': 19082,
            'parentType': 'foo',
            'readOnly': True,
            'title': 'foo'
        })

        assert model.access_level == 'VIEWER'
        assert isinstance(model.comment, smart.models.Comment)
        assert isinstance(model.comment_attachments[0], smart.models.Attachment)
        assert isinstance(model.comments[0], smart.models.Comment)
        assert isinstance(model.created_by, smart.models.User)
        assert model._id == 19082
        assert isinstance(model.last_commented_user, smart.models.User)
        assert model.parent_id == 19082
        assert model.parent_type == 'foo'
        assert model.read_only == True
        assert model.title == 'foo'
        model.comment = {}
        assert isinstance(model.comment, smart.models.Comment)
        model.createdBy = {}
        assert isinstance(model.created_by, smart.models.User)
        model.lastCommentedUser = {}
        assert isinstance(model.last_commented_user, smart.models.User)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_discussion_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Discussion({
            'comment': smart.models.Comment(),
            'comments': smart.models.Comment(),
            'title': 'foo',
            'access_level': 'VIEWER',
            'comment_attachments': smart.models.Attachment(),
            'created_by': smart.models.User(),
            '_id': 19082,
            'last_commented_user': smart.models.User(),
            'parent_id': 19082,
            'parent_type': 'foo',
            'read_only': True
        })

        assert model.access_level == 'VIEWER'
        assert isinstance(model.comment, smart.models.Comment)
        assert isinstance(model.comment_attachments[0], smart.models.Attachment)
        assert isinstance(model.comments[0], smart.models.Comment)
        assert isinstance(model.created_by, smart.models.User)
        assert model._id == 19082
        assert isinstance(model.last_commented_user, smart.models.User)
        assert model.parent_id == 19082
        assert model.parent_type == 'foo'
        assert model.read_only == True
        assert model.title == 'foo'

    def test_attachment(self, smart_setup):
        smart = smart_setup['smart']
        # attachment_sub_type, attachmentSubType
        # attachment_type, attachmentType
        # created_at, createdAt
        # created_by, createdBy
        # description, description
        # _id, id
        # mime_type, mimeType
        # name, name
        # parent_id, parentId
        # parent_type, parentType
        # size_in_kb, sizeInKb
        # url, url
        # url_expires_in_millis, urlExpiresInMillis
        model = smart.models.Attachment({
            'attachmentSubType': 'DOCUMENT',
            'attachmentType': 'BOX_COM',
            'createdBy': smart.models.User(),
            'description': 'foo',
            'id': 19082,
            'mimeType': 'foo',
            'name': 'foo',
            'parentId': 19082,
            'parentType': 'SHEET',
            'sizeInKb': 19082,
            'url': 'foo',
            'urlExpiresInMillis': 19082
        })

        assert model.attachment_sub_type == 'DOCUMENT'
        assert model.attachment_type == 'BOX_COM'
        assert isinstance(model.created_by, smart.models.User)
        assert model.description == 'foo'
        assert model._id == 19082
        assert model.mime_type == 'foo'
        assert model.name == 'foo'
        assert model.parent_id == 19082
        assert model.parent_type == 'SHEET'
        assert model.size_in_kb == 19082
        assert model.url == 'foo'
        assert model.url_expires_in_millis == 19082
        model.createdBy = {}
        assert isinstance(model.created_by, smart.models.User)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_attachment_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.Attachment({
            'description': 'foo',
            'mimeType': 'foo',
            'name': 'foo',
            'parentId': 19082,
            'parentType': 'SHEET',
            'sizeInKb': 19082,
            'url': 'foo',
            'urlExpiresInMillis': 19082,
            'attachment_sub_type': 'DOCUMENT',
            'attachment_type': 'BOX_COM',
            'created_by': smart.models.User(),
            '_id': 19082
        })

        assert model.attachment_sub_type == 'DOCUMENT'
        assert model.attachment_type == 'BOX_COM'
        assert isinstance(model.created_by, smart.models.User)
        assert model.description == 'foo'
        assert model._id == 19082
        assert model.mime_type == 'foo'
        assert model.name == 'foo'
        assert model.parent_id == 19082
        assert model.parent_type == 'SHEET'
        assert model.size_in_kb == 19082
        assert model.url == 'foo'
        assert model.url_expires_in_millis == 19082

    def test_sheet_email(self, smart_setup):
        smart = smart_setup['smart']
        # message, message
        # send_to, sendTo
        # subject, subject
        # format_details, formatDetails
        # _format, format
        # cc_me, ccMe
        model = smart.models.SheetEmail({
            'message': 'foo',
            'sendTo': smart.models.Recipient(),
            'subject': 'foo',
            'formatDetails': smart.models.FormatDetails(),
            'format': 'PDF',
            'ccMe': True
        })

        assert model.message == 'foo'
        assert isinstance(model.send_to[0], smart.models.Recipient)
        assert model.subject == 'foo'
        assert isinstance(model.format_details, smart.models.FormatDetails)
        assert model._format == 'PDF'
        assert model.cc_me == True
        model.formatDetails = {}
        assert isinstance(model.format_details, smart.models.FormatDetails)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_sheet_email_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.SheetEmail({
            'message': 'foo',
            'subject': 'foo',
            'send_to': smart.models.Recipient(),
            'format_details': smart.models.FormatDetails(),
            '_format': 'PDF',
            'cc_me': True
        })

        assert model.message == 'foo'
        assert isinstance(model.send_to[0], smart.models.Recipient)
        assert model.subject == 'foo'
        assert isinstance(model.format_details, smart.models.FormatDetails)
        assert model._format == 'PDF'
        assert model.cc_me == True

    def test_access_token(self, smart_setup):
        smart = smart_setup['smart']
        # access_token, access_token
        # expires_in, expires_in
        # refresh_token, refresh_token
        # token_type, token_type
        model = smart.models.AccessToken({
            'access_token': 'foo',
            'expires_in': 19082,
            'refresh_token': 'foo',
            'token_type': 'bearer'
        })

        assert model.access_token == 'foo'
        assert model.expires_in == 19082
        assert model.refresh_token == 'foo'
        assert model.token_type == 'bearer'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_index_result(self, smart_setup):
        smart = smart_setup['smart']
        # data, data
        # page_number, pageNumber
        # page_size, pageSize
        # total_count, totalCount
        # total_pages, totalPages
        model = smart.models.IndexResult({
            'pageNumber': 19082,
            'pageSize': 19082,
            'totalCount': 19082,
            'totalPages': 19082
        })

        assert model.page_number == 19082
        assert model.page_size == 19082
        assert model.total_count == 19082
        assert model.total_pages == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_index_result_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.IndexResult({
            'page_number': 19082,
            'page_size': 19082,
            'total_count': 19082,
            'total_pages': 19082
        })

        assert model.page_number == 19082
        assert model.page_size == 19082
        assert model.total_count == 19082
        assert model.total_pages == 19082

    def test_cell_history(self, smart_setup):
        smart = smart_setup['smart']
        # link_in_from_cell, linkInFromCell
        # modified_at, modifiedAt
        # column_type, columnType
        # modified_by, modifiedBy
        # hyperlink, hyperlink
        # conditional_format, conditionalFormat
        # value, value
        # column_id, columnId
        # _format, format
        # strict, strict
        # display_value, displayValue
        # links_out_to_cells, linksOutToCells
        # formula, formula
        model = smart.models.CellHistory({
            'linkInFromCell': smart.models.CellLink(),
            'columnType': 'foo',
            'modifiedBy': smart.models.User(),
            'hyperlink': smart.models.Hyperlink(),
            'conditionalFormat': 'foo',
            'value': 'foo',
            'columnId': 19082,
            'format': 'foo',
            'strict': True,
            'displayValue': 'foo',
            'linksOutToCells': smart.models.CellLink(),
            'formula': 'foo'
        })

        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        assert model.column_type == 'foo'
        assert isinstance(model.modified_by, smart.models.User)
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        assert model.conditional_format == 'foo'
        assert model.value == 'foo'
        assert model.column_id == 19082
        assert model._format == 'foo'
        assert model.strict == True
        assert model.display_value == 'foo'
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        assert model.formula == 'foo'
        model.linkInFromCell = {}
        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        model.modifiedBy = {}
        assert isinstance(model.modified_by, smart.models.User)
        model.hyperlink = {}
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        model.linksOutToCells = {}
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_cell_history_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.CellHistory({
            'columnType': 'foo',
            'hyperlink': smart.models.Hyperlink(),
            'conditionalFormat': 'foo',
            'value': 'foo',
            'strict': True,
            'displayValue': 'foo',
            'formula': 'foo',
            'link_in_from_cell': smart.models.CellLink(),
            'modified_by': smart.models.User(),
            'column_id': 19082,
            '_format': 'foo',
            'links_out_to_cells': smart.models.CellLink()
        })

        assert isinstance(model.link_in_from_cell, smart.models.CellLink)
        assert model.column_type == 'foo'
        assert isinstance(model.modified_by, smart.models.User)
        assert isinstance(model.hyperlink, smart.models.Hyperlink)
        assert model.conditional_format == 'foo'
        assert model.value == 'foo'
        assert model.column_id == 19082
        assert model._format == 'foo'
        assert model.strict == True
        assert model.display_value == 'foo'
        assert isinstance(model.links_out_to_cells[0], smart.models.CellLink)
        assert model.formula == 'foo'

    def test_user_profile(self, smart_setup):
        smart = smart_setup['smart']
        # account, account
        # admin, admin
        # email, email
        # first_name, firstName
        # group_admin, groupAdmin
        # _id, id
        # last_name, lastName
        # licensed_sheet_creator, licensedSheetCreator
        # locale, locale
        # resource_viewer, resourceViewer
        # status, status
        # time_zone, timeZone
        model = smart.models.UserProfile({
            'account': smart.models.Account(),
            'admin': True,
            'email': 'foo',
            'firstName': 'foo',
            'groupAdmin': True,
            'id': 19082,
            'lastName': 'foo',
            'licensedSheetCreator': True,
            'locale': 'foo',
            'resourceViewer': True,
            'status': 'ACTIVE',
            'timeZone': 'foo'
        })

        assert isinstance(model.account, smart.models.Account)
        assert model.admin == True
        assert model.email == 'foo'
        assert model.first_name == 'foo'
        assert model.group_admin == True
        assert model._id == 19082
        assert model.last_name == 'foo'
        assert model.licensed_sheet_creator == True
        assert model.locale == 'foo'
        assert model.resource_viewer == True
        assert model.status == 'ACTIVE'
        assert model.time_zone == 'foo'
        model.account = {}
        assert isinstance(model.account, smart.models.Account)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_user_profile_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.UserProfile({
            'account': smart.models.Account(),
            'admin': True,
            'email': 'foo',
            'locale': 'foo',
            'status': 'ACTIVE',
            'first_name': 'foo',
            'group_admin': True,
            '_id': 19082,
            'last_name': 'foo',
            'licensed_sheet_creator': True,
            'resource_viewer': True,
            'time_zone': 'foo'
        })

        assert isinstance(model.account, smart.models.Account)
        assert model.admin == True
        assert model.email == 'foo'
        assert model.first_name == 'foo'
        assert model.group_admin == True
        assert model._id == 19082
        assert model.last_name == 'foo'
        assert model.licensed_sheet_creator == True
        assert model.locale == 'foo'
        assert model.resource_viewer == True
        assert model.status == 'ACTIVE'
        assert model.time_zone == 'foo'

    def test_group_member(self, smart_setup):
        smart = smart_setup['smart']
        # email, email
        # first_name, firstName
        # _id, id
        # last_name, lastName
        # name, name
        model = smart.models.GroupMember({
            'email': 'foo',
            'firstName': 'foo',
            'id': 19082,
            'lastName': 'foo',
            'name': 'foo'
        })

        assert model.email == 'foo'
        assert model.first_name == 'foo'
        assert model._id == 19082
        assert model.last_name == 'foo'
        assert model.name == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_group_member_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.GroupMember({
            'email': 'foo',
            'name': 'foo',
            'first_name': 'foo',
            '_id': 19082,
            'last_name': 'foo'
        })

        assert model.email == 'foo'
        assert model.first_name == 'foo'
        assert model._id == 19082
        assert model.last_name == 'foo'
        assert model.name == 'foo'

    def test_error_result(self, smart_setup):
        smart = smart_setup['smart']
        # code, code
        # message, message
        # name, name
        # recommendation, recommendation
        # should_retry, shouldRetry
        # status_code, statusCode
        model = smart.models.ErrorResult({
            'code': 19082,
            'message': 'foo',
            'name': 'foo',
            'recommendation': 'foo',
            'shouldRetry': True,
            'statusCode': 19082
        })

        assert model.code == 19082
        assert model.message == 'foo'
        assert model.name == 'foo'
        assert model.recommendation == 'foo'
        assert model.should_retry == True
        assert model.status_code == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_error_result_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.ErrorResult({
            'code': 19082,
            'message': 'foo',
            'name': 'foo',
            'recommendation': 'foo',
            'should_retry': True,
            'status_code': 19082
        })

        assert model.code == 19082
        assert model.message == 'foo'
        assert model.name == 'foo'
        assert model.recommendation == 'foo'
        assert model.should_retry == True
        assert model.status_code == 19082

    def test_report_column(self, smart_setup):
        smart = smart_setup['smart']
        # sheet_name_column, sheetNameColumn
        # tags, tags
        # index, index
        # symbol, symbol
        # width, width
        # _format, format
        # _type, type
        # _id, id
        # title, title
        # locked_for_user, lockedForUser
        # hidden, hidden
        # primary, primary
        # system_column_type, systemColumnType
        # locked, locked
        # virtual_id, virtualId
        # _filter, filter
        # options, options
        # auto_number_format, autoNumberFormat
        model = smart.models.ReportColumn({
            'sheetNameColumn': True,
            'tags': ['foo'],
            'index': 19082,
            'symbol': 'STAR',
            'width': 19082,
            'format': 'foo',
            'type': 'TEXT_NUMBER',
            'id': 19082,
            'title': 'foo',
            'lockedForUser': True,
            'hidden': True,
            'primary': True,
            'systemColumnType': 'AUTO_NUMBER',
            'locked': True,
            'virtualId': 19082,
            'filter': smart.models.Filter(),
            'options': ['foo'],
            'autoNumberFormat': smart.models.AutoNumberFormat()
        })

        assert model.sheet_name_column == True
        assert model.tags[0] == 'foo'
        assert model.index == 19082
        assert model.symbol == 'STAR'
        assert model.width == 19082
        assert model._format == 'foo'
        assert model._type == 'TEXT_NUMBER'
        assert model._id == 19082
        assert model.title == 'foo'
        assert model.locked_for_user == True
        assert model.hidden == True
        assert model.primary == True
        assert model.system_column_type == 'AUTO_NUMBER'
        assert model.locked == True
        assert model.virtual_id == 19082
        assert isinstance(model._filter, smart.models.Filter)
        assert model.options[0] == 'foo'
        assert isinstance(model.auto_number_format, smart.models.AutoNumberFormat)
        model.tags = 'foo'
        assert model.tags[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.tags = tmplist
        assert model.tags[0] == 'foo'
        model.filter = {}
        assert isinstance(model._filter, smart.models.Filter)
        model.options = 'foo'
        assert model.options[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.options = tmplist
        assert model.options[0] == 'foo'
        model.autoNumberFormat = {}
        assert isinstance(model.auto_number_format, smart.models.AutoNumberFormat)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_report_column_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.ReportColumn({
            'tags': ['foo'],
            'index': 19082,
            'symbol': 'STAR',
            'width': 19082,
            'title': 'foo',
            'hidden': True,
            'primary': True,
            'locked': True,
            'options': ['foo'],
            'sheet_name_column': True,
            '_format': 'foo',
            '_type': 'TEXT_NUMBER',
            '_id': 19082,
            'locked_for_user': True,
            'system_column_type': 'AUTO_NUMBER',
            'virtual_id': 19082,
            '_filter': smart.models.Filter(),
            'auto_number_format': smart.models.AutoNumberFormat()
        })

        assert model.sheet_name_column == True
        assert model.tags[0] == 'foo'
        assert model.index == 19082
        assert model.symbol == 'STAR'
        assert model.width == 19082
        assert model._format == 'foo'
        assert model._type == 'TEXT_NUMBER'
        assert model._id == 19082
        assert model.title == 'foo'
        assert model.locked_for_user == True
        assert model.hidden == True
        assert model.primary == True
        assert model.system_column_type == 'AUTO_NUMBER'
        assert model.locked == True
        assert model.virtual_id == 19082
        assert isinstance(model._filter, smart.models.Filter)
        assert model.options[0] == 'foo'
        assert isinstance(model.auto_number_format, smart.models.AutoNumberFormat)

    def test_search_result(self, smart_setup):
        smart = smart_setup['smart']
        # results, results
        # total_count, totalCount
        model = smart.models.SearchResult({
            'results': smart.models.SearchResultItem(),
            'totalCount': 19082
        })

        assert isinstance(model.results[0], smart.models.SearchResultItem)
        assert model.total_count == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_search_result_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.SearchResult({
            'results': smart.models.SearchResultItem(),
            'totalCount': 19082
        })

        assert isinstance(model.results[0], smart.models.SearchResultItem)
        assert model.total_count == 19082

    def test_sheet_publish(self, smart_setup):
        smart = smart_setup['smart']
        # ical_enabled, icalEnabled
        # ical_url, icalUrl
        # read_only_full_enabled, readOnlyFullEnabled
        # read_only_full_url, readOnlyFullUrl
        # read_only_lite_enabled, readOnlyLiteEnabled
        # read_only_lite_url, readOnlyLiteUrl
        # read_write_enabled, readWriteEnabled
        # read_write_url, readWriteUrl
        model = smart.models.SheetPublish({
            'icalEnabled': True,
            'icalUrl': 'foo',
            'readOnlyFullEnabled': True,
            'readOnlyFullUrl': 'foo',
            'readOnlyLiteEnabled': True,
            'readOnlyLiteUrl': 'foo',
            'readWriteEnabled': True,
            'readWriteUrl': 'foo'
        })

        assert model.ical_enabled == True
        assert model.ical_url == 'foo'
        assert model.read_only_full_enabled == True
        assert model.read_only_full_url == 'foo'
        assert model.read_only_lite_enabled == True
        assert model.read_only_lite_url == 'foo'
        assert model.read_write_enabled == True
        assert model.read_write_url == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_sheet_publish_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.SheetPublish({
            'icalUrl': 'foo',
            'readOnlyFullUrl': 'foo',
            'readOnlyLiteUrl': 'foo',
            'readWriteUrl': 'foo',
            'ical_enabled': True,
            'read_only_full_enabled': True,
            'read_only_lite_enabled': True,
            'read_write_enabled': True
        })

        assert model.ical_enabled == True
        assert model.ical_url == 'foo'
        assert model.read_only_full_enabled == True
        assert model.read_only_full_url == 'foo'
        assert model.read_only_lite_enabled == True
        assert model.read_only_lite_url == 'foo'
        assert model.read_write_enabled == True
        assert model.read_write_url == 'foo'

    def test_format_tables(self, smart_setup):
        smart = smart_setup['smart']
        # bold, bold
        # color, color
        # currency, currency
        # decimal_count, decimalCount
        # defaults, defaults
        # font_family, fontFamily
        # font_size, fontSize
        # horizontal_align, horizontalAlign
        # italic, italic
        # number_format, numberFormat
        # strikethrough, strikethrough
        # text_wrap, textWrap
        # thousands_separator, thousandsSeparator
        # underline, underline
        # vertical_align, verticalAlign
        model = smart.models.FormatTables({
            'bold': ['foo'],
            'color': ['foo'],
            'currency': smart.models.Currency(),
            'decimalCount': ['foo'],
            'defaults': 'foo',
            'fontFamily': smart.models.FontFamily(),
            'fontSize': ['foo'],
            'horizontalAlign': ['foo'],
            'italic': ['foo'],
            'numberFormat': ['foo'],
            'strikethrough': ['foo'],
            'textWrap': ['foo'],
            'thousandsSeparator': ['foo'],
            'underline': ['foo'],
            'verticalAlign': ['foo']
        })

        assert model.bold[0] == 'foo'
        assert model.color[0] == 'foo'
        assert isinstance(model.currency[0], smart.models.Currency)
        assert model.decimal_count[0] == 'foo'
        assert model.defaults == 'foo'
        assert isinstance(model.font_family[0], smart.models.FontFamily)
        assert model.font_size[0] == 'foo'
        assert model.horizontal_align[0] == 'foo'
        assert model.italic[0] == 'foo'
        assert model.number_format[0] == 'foo'
        assert model.strikethrough[0] == 'foo'
        assert model.text_wrap[0] == 'foo'
        assert model.thousands_separator[0] == 'foo'
        assert model.underline[0] == 'foo'
        assert model.vertical_align[0] == 'foo'
        model.bold = 'foo'
        assert model.bold[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.bold = tmplist
        assert model.bold[0] == 'foo'
        model.color = 'foo'
        assert model.color[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.color = tmplist
        assert model.color[0] == 'foo'
        model.decimal_count = 'foo'
        assert model.decimal_count[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.decimal_count = tmplist
        assert model.decimal_count[0] == 'foo'
        model.font_size = 'foo'
        assert model.font_size[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.font_size = tmplist
        assert model.font_size[0] == 'foo'
        model.horizontal_align = 'foo'
        assert model.horizontal_align[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.horizontal_align = tmplist
        assert model.horizontal_align[0] == 'foo'
        model.italic = 'foo'
        assert model.italic[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.italic = tmplist
        assert model.italic[0] == 'foo'
        model.number_format = 'foo'
        assert model.number_format[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.number_format = tmplist
        assert model.number_format[0] == 'foo'
        model.strikethrough = 'foo'
        assert model.strikethrough[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.strikethrough = tmplist
        assert model.strikethrough[0] == 'foo'
        model.text_wrap = 'foo'
        assert model.text_wrap[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.text_wrap = tmplist
        assert model.text_wrap[0] == 'foo'
        model.thousands_separator = 'foo'
        assert model.thousands_separator[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.thousands_separator = tmplist
        assert model.thousands_separator[0] == 'foo'
        model.underline = 'foo'
        assert model.underline[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.underline = tmplist
        assert model.underline[0] == 'foo'
        model.vertical_align = 'foo'
        assert model.vertical_align[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.vertical_align = tmplist
        assert model.vertical_align[0] == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_format_tables_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.FormatTables({
            'bold': ['foo'],
            'color': ['foo'],
            'currency': smart.models.Currency(),
            'defaults': 'foo',
            'italic': ['foo'],
            'strikethrough': ['foo'],
            'underline': ['foo'],
            'decimal_count': ['foo'],
            'font_family': smart.models.FontFamily(),
            'font_size': ['foo'],
            'horizontal_align': ['foo'],
            'number_format': ['foo'],
            'text_wrap': ['foo'],
            'thousands_separator': ['foo'],
            'vertical_align': ['foo']
        })

        assert model.bold[0] == 'foo'
        assert model.color[0] == 'foo'
        assert isinstance(model.currency[0], smart.models.Currency)
        assert model.decimal_count[0] == 'foo'
        assert model.defaults == 'foo'
        assert isinstance(model.font_family[0], smart.models.FontFamily)
        assert model.font_size[0] == 'foo'
        assert model.horizontal_align[0] == 'foo'
        assert model.italic[0] == 'foo'
        assert model.number_format[0] == 'foo'
        assert model.strikethrough[0] == 'foo'
        assert model.text_wrap[0] == 'foo'
        assert model.thousands_separator[0] == 'foo'
        assert model.underline[0] == 'foo'
        assert model.vertical_align[0] == 'foo'

    def test_update_request(self, smart_setup):
        smart = smart_setup['smart']
        # _id, id
        model = smart.models.UpdateRequest({
            'id': 19082
        })

        assert model._id == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_update_request_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.UpdateRequest({
            '_id': 19082
        })

        assert model._id == 19082

    def test_format_details(self, smart_setup):
        smart = smart_setup['smart']
        # paper_size, paperSize
        model = smart.models.FormatDetails({
            'paperSize': 'LETTER'
        })

        assert model.paper_size == 'LETTER'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_format_details_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.FormatDetails({
            'paper_size': 'LETTER'
        })

        assert model.paper_size == 'LETTER'

    def test_multi_row_email(self, smart_setup):
        smart = smart_setup['smart']
        # row_ids, rowIds
        model = smart.models.MultiRowEmail({
            'rowIds': [19082]
        })

        assert model.row_ids[0] == 19082
        model.row_ids = 19082
        assert model.row_ids[0] == 19082
        tmplist = smartsheet.types.TypedList(int)
        tmplist.append(19082)
        model.row_ids = tmplist
        assert model.row_ids[0] == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_multi_row_email_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.MultiRowEmail({
            'row_ids': [19082]
        })

        assert model.row_ids[0] == 19082

    def test_downloaded_file(self, smart_setup):
        smart = smart_setup['smart']
        # download_directory, downloadDirectory
        # filename, filename
        # message, message
        # resp, resp
        # result_code, resultCode
        model = smart.models.DownloadedFile({
            'downloadDirectory': 'foo',
            'filename': 'foo',
            'message': 'foo',
            'resultCode': 19082
        })

        assert model.download_directory == 'foo'
        assert model.filename == 'foo'
        assert model.message == 'foo'
        assert model.result_code == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_downloaded_file_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.DownloadedFile({
            'filename': 'foo',
            'message': 'foo',
            'resultCode': 19082,
            'download_directory': 'foo'
        })

        assert model.download_directory == 'foo'
        assert model.filename == 'foo'
        assert model.message == 'foo'
        assert model.result_code == 19082

    def test_alternate_email(self, smart_setup):
        smart = smart_setup['smart']
        # confirmed, confirmed
        # email, email
        # _id, id
        model = smart.models.AlternateEmail({
            'confirmed': True,
            'email': 'foo',
            'id': 19082
        })

        assert model.confirmed == True
        assert model.email == 'foo'
        assert model._id == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_alternate_email_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.AlternateEmail({
            'confirmed': True,
            'email': 'foo',
            'id': 19082
        })

        assert model.confirmed == True
        assert model.email == 'foo'
        assert model._id == 19082

    def test_search_result_item(self, smart_setup):
        smart = smart_setup['smart']
        # context_data, contextData
        # object_id, objectId
        # object_type, objectType
        # parent_object_id, parentObjectId
        # parent_object_name, parentObjectName
        # parent_object_type, parentObjectType
        # text, text
        model = smart.models.SearchResultItem({
            'contextData': ['foo'],
            'objectId': 19082,
            'objectType': 'row',
            'parentObjectId': 19082,
            'parentObjectName': 'foo',
            'parentObjectType': 'workspace',
            'text': 'foo'
        })

        assert model.context_data[0] == 'foo'
        assert model.object_id == 19082
        assert model.object_type == 'row'
        assert model.parent_object_id == 19082
        assert model.parent_object_name == 'foo'
        assert model.parent_object_type == 'workspace'
        assert model.text == 'foo'
        model.context_data = 'foo'
        assert model.context_data[0] == 'foo'
        tmplist = smartsheet.types.TypedList(str)
        tmplist.append('foo')
        model.context_data = tmplist
        assert model.context_data[0] == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_search_result_item_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.SearchResultItem({
            'objectId': 19082,
            'objectType': 'row',
            'parentObjectId': 19082,
            'parentObjectName': 'foo',
            'parentObjectType': 'workspace',
            'text': 'foo',
            'context_data': ['foo']
        })

        assert model.context_data[0] == 'foo'
        assert model.object_id == 19082
        assert model.object_type == 'row'
        assert model.parent_object_id == 19082
        assert model.parent_object_name == 'foo'
        assert model.parent_object_type == 'workspace'
        assert model.text == 'foo'

    def test_auto_number_format(self, smart_setup):
        smart = smart_setup['smart']
        # fill, fill
        # prefix, prefix
        # starting_number, startingNumber
        # suffix, suffix
        model = smart.models.AutoNumberFormat({
            'fill': 'foo',
            'prefix': 'foo',
            'startingNumber': 19082,
            'suffix': 'foo'
        })

        assert model.fill == 'foo'
        assert model.prefix == 'foo'
        assert model.starting_number == 19082
        assert model.suffix == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_auto_number_format_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.AutoNumberFormat({
            'fill': 'foo',
            'prefix': 'foo',
            'suffix': 'foo',
            'starting_number': 19082
        })

        assert model.fill == 'foo'
        assert model.prefix == 'foo'
        assert model.starting_number == 19082
        assert model.suffix == 'foo'

    def test_sheet_user_settings(self, smart_setup):
        smart = smart_setup['smart']
        # critical_path_enabled, criticalPathEnabled
        model = smart.models.SheetUserSettings({
            'criticalPathEnabled': True
        })

        assert model.critical_path_enabled == True
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_sheet_user_settings_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.SheetUserSettings({
            'critical_path_enabled': True
        })

        assert model.critical_path_enabled == True

    def test_copy_or_move_row_result(self, smart_setup):
        smart = smart_setup['smart']
        # destination_sheet_id, destinationSheetId
        # row_mappings, rowMappings
        model = smart.models.CopyOrMoveRowResult({
            'destinationSheetId': 19082,
            'rowMappings': smart.models.RowMapping()
        })

        assert model.destination_sheet_id == 19082
        assert isinstance(model.row_mappings[0], smart.models.RowMapping)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_copy_or_move_row_result_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.CopyOrMoveRowResult({
            'destination_sheet_id': 19082,
            'row_mappings': smart.models.RowMapping()
        })

        assert model.destination_sheet_id == 19082
        assert isinstance(model.row_mappings[0], smart.models.RowMapping)

    def test_container_destination(self, smart_setup):
        smart = smart_setup['smart']
        # destination_id, destinationId
        # destination_type, destinationType
        # new_name, newName
        model = smart.models.ContainerDestination({
            'destinationId': 19082,
            'destinationType': 'home',
            'newName': 'foo'
        })

        assert model.destination_id == 19082
        assert model.destination_type == 'home'
        assert model.new_name == 'foo'
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_container_destination_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.ContainerDestination({
            'destination_id': 19082,
            'destination_type': 'home',
            'new_name': 'foo'
        })

        assert model.destination_id == 19082
        assert model.destination_type == 'home'
        assert model.new_name == 'foo'

    def test_copy_or_move_row_directive(self, smart_setup):
        smart = smart_setup['smart']
        # row_ids, rowIds
        # to, to
        model = smart.models.CopyOrMoveRowDirective({
            'rowIds': [19082],
            'to': smart.models.CopyOrMoveRowDestination()
        })

        assert model.row_ids[0] == 19082
        assert isinstance(model.to, smart.models.CopyOrMoveRowDestination)
        model.row_ids = 19082
        assert model.row_ids[0] == 19082
        tmplist = smartsheet.types.TypedList(int)
        tmplist.append(19082)
        model.row_ids = tmplist
        assert model.row_ids[0] == 19082
        model.to = {}
        assert isinstance(model.to, smart.models.CopyOrMoveRowDestination)
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_copy_or_move_row_directive_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.CopyOrMoveRowDirective({
            'to': smart.models.CopyOrMoveRowDestination(),
            'row_ids': [19082]
        })

        assert model.row_ids[0] == 19082
        assert isinstance(model.to, smart.models.CopyOrMoveRowDestination)

    def test_copy_or_move_row_destination(self, smart_setup):
        smart = smart_setup['smart']
        # sheet_id, sheetId
        model = smart.models.CopyOrMoveRowDestination({
            'sheetId': 19082
        })

        assert model.sheet_id == 19082
        as_dict = model.to_dict()
        assert isinstance(as_dict, dict)

    def test_copy_or_move_row_destination_snake(self, smart_setup):
        smart = smart_setup['smart']
        model = smart.models.CopyOrMoveRowDestination({
            'sheet_id': 19082
        })

        assert model.sheet_id == 19082
