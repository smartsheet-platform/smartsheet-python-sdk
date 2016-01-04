import smartsheet

#
# Create Folder in Sheets Folder (Home)
#

smart = smartsheet.Smartsheet()
folder = smart.Home.create_folder('Python SDK Folder A')
print(folder)
