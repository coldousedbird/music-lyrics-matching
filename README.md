# music-lyrics-matching

App, which retrieves synchronized lyrics from *.mp3*. Output is [*.LRC-file*](https://en.wikipedia.org/wiki/LRC_(file_format)) - lyrics + timestamps.

App uses such libs as:
- PyQT6 for graphical interface
- SQLite for local database 
- pydub and librosa for operations with audio 

## Contents
- [Installation](##Installation)
- [Usage](##Usage)
- [Project structure](##Structure)
- [Contributing](##Contributing)
- [License](##License)

## Installation

- Make sure, that your machine has installed the most latest version of python (I used 3.12.3)

- Obviously, you need to install [pip](https://pip.pypa.io/en/stable/), if you don't have it yet.
```bash
python3 get-pip.py
```

- Clone repository and move to directory
```bash 
git clone https://github.com/coldousedbird/music-lyrics-matching.git
cd music-lyrics-matching
```

- Create and activate python virtual environment
```bash
# Windows
python -m venv mlm-venv
mlm-venv\Scripts\activate.bat
```
```bash
# Linux:
python -m venv mlm-venv
source ./mlm-venv/bin/activate
```

- Use pip to install dependencies
```bash
pip install -r requirements.txt
```


## Usage

- Start app
```bash
python src/App.py
```

- On initial startup, app will create empty sqlite3 database - *.db-file*. 
- In Processing tab, choose *.mp3-file* through context menu 
- Press button "Recognize" to get *.lrc-file*.
- Once file is processed, request is saved to your local database and can be removed or downloaded again
+ You can also run other files in **src/** directory - it will activate simple testing script for this class. 
```bash
# Testing files
python src/ProcessingTab.py
python src/HistoryTab.py
python src/Processing.py
python src/RequestDB.py
```

## Structure

Repository contains 
- **src** - source code files
  - **others** - scripts for datasets 
  - **model** - notebooks for model creation
  - *App.py* - main window class.
  - *ProcessingTab.py* - process tab class
  - *HistoryTab.py* - history tab class
  - *Processing.py* - processing module class
  - *RequestsDB.py* - database communication class
- **schemes** - scheme images
- *.gitignore* - ignored files
- *LICENSE* - GNU GPL-3.0 license
- *README.md* - this exact text written here
 
## Contributing

Pull requests are welcome. For major changes, please open an issue first
to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[GNU GPL-3.0](https://choosealicense.com/licenses/gpl-3.0/)