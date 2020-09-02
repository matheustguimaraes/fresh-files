import datetime
import os
import sys
import time
from pathlib import Path

from dateutil.relativedelta import relativedelta
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

while True:
    try:
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
            print('Usage: upload_to_gdrive.py '
                  '[source dir] '
                  '[file type] '
                  '[gdrive folder id]')
            print('Example: python upload_to_gdrive.py'
                  ' images/ jgp 12lp12l4p')
            break

        pathDirSource = sys.argv[1]  # 'sourceDir'
        extension_files = sys.argv[2]  # 'mp4'
        id_drive = sys.argv[3]  # 12lp12l4p125k12o215k

        now = datetime.date.today()
        two_m_ago = now - relativedelta(months=2)
        time_limit = time.mktime(two_m_ago.timetuple())

        files = Path(pathDirSource).glob('**/*.' + extension_files)

        if extension_files == 'txt':
            opening_mode = 'r'
        else:
            opening_mode = 'rb'

        for f in files:
            if not files:
                break
            directories = str(f).rsplit('/', 1)[0].split('/')
            file_name = str(f).rsplit('/', 1)[1]

            # Continue if modified time is bigger than 2 months
            mod_file_time = os.stat(f).st_mtime
            mod_days = time.ctime(os.stat(f).st_mtime)

            if mod_file_time > time_limit:
                continue

            print("[INFO]",
                  datetime.datetime.now(),
                  "| file:", f,
                  "| file date:", time.ctime(mod_file_time),
                  "| limit:", time.ctime(time_limit),
                  )
            if extension_files == 'txt':
                with open(str(f), opening_mode) as file_open:
                    file_drive = drive.CreateFile({'title': file_name,
                                                   'parents': [{"id": id_drive}]})
                    file_drive.SetContentString(file_open.read())
            else:
                file_drive = drive.CreateFile({'title': file_name,
                                               'parents': [{"id": id_drive}]})
                file_drive.SetContentFile(str(f))
            file_drive.Upload()

            fn = os.path.basename(f)
            if file_drive["id"] is not None:
                print("[INFO] The file: " + fn + " was uploaded.")
                try:
                    os.remove(f)
                    print("[INFO] The file: " + fn + " was removed from the hard disk.")
                except OSError as error:
                    print(error)
                    print("[ERROR] The file: " + fn + " was not removed from the hard disk.")
            else:
                print("[ERROR] Upload failed to the file: " + fn + ". drive[id] not found")
        break
    except Exception as ex:
        print(ex)

print("[END] Script was finished")
