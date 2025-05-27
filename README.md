# CCI - London Tech Week - Print

## Install

1. Create conda environment:  
`conda create -n ltw-print python=3.11`

2. Activate conda environment:  
`conda activate ltw-print`

3. Install requirments:  
`python -m pip install -r .\requirments.txt`

Done.

## Running the server

1. Start the python HTTP server (Make sure conda env is activated)  
`python .\server.py`

## Debug

### Server runs but no printing

- Check correct COM port for serial printer
    1. Open windows device manager (Right click start button, select device manager)
    2. Look for `Ports (COM & LPT)`
    3. edit print.py - line 17-21 settings object

- Check serial cable is plugged in fully and not damaged
- Check printer has paper, is switched on and not blocked