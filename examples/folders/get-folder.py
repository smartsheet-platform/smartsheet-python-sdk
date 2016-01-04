import smartsheet

#
# Get folder
#
# Dependencies: examples.home.create-folder
#

smart = smartsheet.Smartsheet()
folder_id = 000000000
action = smart.Folders.get_folder(folder_id)
folders = action.result
print(folders)
