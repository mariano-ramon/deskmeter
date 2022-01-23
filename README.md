# Deskmeter

Deskmeter is a productivity tool to measure how much time you spend doing stuff in your computer.
More precisely how much time passes while a given workspace is active.

## Requirements

- MongoDB
- wmctrl
- Flask

install those first, also wmctrl doesn't work on wayland, until an equivalent is found. you have to switch to XORG.

## Define Workspace Labels

edit the desktops variable in `dmmain.py` to your needs, first is workspace 1, second 2 and so on

## How to run

leave the dmmain.py running in the background, use the dmapp flask application to see the data.
the homepage shows current day result, 
`/calendar` shows the current month with week totals
`/calendar/<month_number>` shows the select month of current year with week totals
`/calendar/<month_number>` shows the select month of current year with week totals

adapt `deskmeter.sh` and `dmapp.sh` to your needs. I put those in my home directory. Add starting the mongo service 