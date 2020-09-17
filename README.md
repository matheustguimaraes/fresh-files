# fresh-files
This script uploads files older than two months to Google Drive and then deletes them from the local computer.

## Installing
Create python virtual environment:
```sh
python3 -m venv .env
source .env/bin/activate
pip install -r requirements.txt
```
and get Google Drive credentials ```mycred.txt``` and ```client_secrets.json``` at https://developers.google.com/drive.

## Running
Open tmux session, execute script and detach from the session:

```sh
tmux # create tmux session
cd <path/to/project>
source .env/bin/activate # use installed virtual environment
python upload_to_gdrive.py \
    <path/to/files/to/upload> \
    <filesFormat> \
    <gDriveFolderID>
    
example:
    python upload_to_gdrive.py ./dataset jgp 12lp12l4p 

<C-b> d # detach from the session
```

or, run script in crontab:

```sh
crontab -e # open user crontab
@reboot /path/to/script/.env/bin/python3 upload_to_gdrive.py ./dataset jgp 12lp12l4p
```

## License
[MIT](LICENSE.md)
