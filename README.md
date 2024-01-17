# PyShot

This project was created for the subject 'Introduction to programming' at Vistula University.

PyShot is an app for creating cropped screenshots of your main display.

Similarly to Windows 10 built-in Snipping tool, PyShot can make a screenshot when a key combination is pressed and allow to instantly crop it however you need. The cropped screenshot is automatically saved to the clipboard.

## Requirements

This projects runs on Windows 10 or Windows 11 and requires Python 3 installed (written using python 3.12.1, tested on Windows 10).

## Installation

Create and activate a [virtual environment](https://docs.python.org/3/library/venv.html):
```powershell
make init

# or

python -m venv .venv; .\.venv\Scripts\activate
```

Install dependencies:
```powershell
make install

# or

pip install -r requirements.txt
```

You can now run the script:
```powershell
python main.py
```

## Usage

### Making a screenshot

Once you run the script press `Win + Ctrl + Shift + s`.
The screen should become darker and a red border should appear.

![Image not found!](docs/demo.png?raw=true)

Select the area to save by clicking and holding LPM.
Once the LPM is released the selected area will be saved to clipboard.


![Image not found!](docs/demo2.png?raw=true)

You can now paste the screenshot wherever you need.

![Image not found!](docs/demo3.png?raw=true)
![Image not found!](docs/demo4.png?raw=true)

### How to turn it off

In order to turn off PyShot and stop it from listening for the  `Win + Ctrl + Shift + s` key combination 
just get back to the terminal where it was started and press `Ctrl + c` or kill the process from the Task Manager.
