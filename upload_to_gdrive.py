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
        gauth = GoogleAuth()
        gauth.LoadCredentialsFile("mycreds.txt")

        if gauth.credentials is None:
            gauth.LocalWebserverAuth()
        elif gauth.access_token_expired:
            gauth.Refresh()
        else:
            gauth.Authorize()

        gauth.SaveCredentialsFile("mycreds.txt")
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

        pathDirSource = sys.argv[1]
        extension_files = sys.argv[2]
        id_drive = sys.argv[3]

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
                print("[INFO] Uploaded: " + fn)
                try:
                    os.remove(f)
                    print("[INFO] Removed from disk: " + fn)
                except OSError as error:
                    print(error)
                    print("[ERROR] Error, failed to upload due to OS error: " + fn)
            else:
                print("[ERROR] Failed to upload: " + fn)
        break
    except Exception as ex:
        print(ex)

print("[END] Script was finished")
