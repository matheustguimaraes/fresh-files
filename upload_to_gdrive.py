import os
import sys
from pathlib import Path

from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

# AM: Login to Google Drive and create drive object
gauth = GoogleAuth()

# Automatic autentication
# AM: Try to load saved client credentials
gauth.LoadCredentialsFile("mycreds.txt")

if gauth.credentials is None:
    # Authenticate if they're not there
    gauth.LocalWebserverAuth()
elif gauth.access_token_expired:
    # Refresh them if expired
    gauth.Refresh()
else:
    # Initialize the saved creds
    gauth.Authorize()
# Save the current credentials to a file
gauth.SaveCredentialsFile("mycreds.txt")

# End Automatic autentication
drive = GoogleDrive(gauth)
gauth.LocalWebserverAuth()

if len(sys.argv) < 4:
    print('Usage: gotoDrive.py '
          '[source dir] '
          '[file type] '
          '[gdrive folder id]')

pathDirSource = sys.argv[1]  # 'sourceDir'
extensionFiles = sys.argv[2]  # 'mp4'
id_drive = sys.argv[3]  # 12lp12l4p125k12o215k

# pathFull = pathDirSource+'/'+'*.'+extensionFiles
# Searching files
# files = glob.glob(pathFull)
files = Path(pathDirSource).glob('**/*.' + extensionFiles)

print('files:', files)

# if len(files) < 1:
#    print("[WARN] Files not found!")
# else:
dic_path = {}
for f in files:

    directories = str(f).rsplit('/', 1)[0].split('/')
    # directories = str(file).rsplit('/', 1)[0].rsplit('/',1)[1]

    idParent = id_drive

    fileName = str(f).rsplit('/', 1)[1]
    print('filename', fileName)

    if extensionFiles == 'txt':
        openingMode = 'r'
    else:
        openingMode = 'rb'

    print('open', openingMode)

    with open(str(f), openingMode) as file_open:
        try:
            print(openingMode, fileName)
            fn = os.path.basename(file_open.name)
            file_drive = drive.CreateFile({'title': fileName,
                                           'parents': [{"id": id_drive}]})
            if extensionFiles == 'txt':
                file_drive.SetContentString(file_open.read())
            else:
                print('f', file_open)
                file_drive.SetContentFile(str(file_open.name))
            file_drive.Upload()

            if file_drive["id"] is not None:
                print("[OK] The file: " + fn + " has been uploaded.")
                try:
                    os.remove(str(f))
                    print("[OK] The file: " + fn + " has been removed of the hard disk.")
                except OSError as error:
                    print(error)
                    print("[ERROR] The file: " + fn + " cannot be removed of the hard disk.")
            else:
                print("[ERROR] Upload faill to the file: " + fn + "!")

        except Exception as ex:
            print("[ERROR] Exception:", sys.exc_info()[0], "occured.")
            raise

# for removeDir in dicPath.keys():
# shutil.rmtree(removeDir)

print("-------------------------------")
print("Finished!")
print("-------------------------------")
