import smartsheet

#
# List folders
#

smart = smartsheet.Smartsheet()
action = smart.Home.list_folders(include_all=True)
folders = action.result
print(folders)
