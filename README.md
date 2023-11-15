# pararius-apartments-alert
Scraping and notification application for pararius.nl

##
NOTICE: this is a personal project and it has not been/is not being developed with a pleasasant nor straightforward user experience in mind. The code is also not following industry standards because there is no need to. I'm developing this for fun to see if I can reproduce the service [Pararius+](https://www.pararius.nl/info/parariusplus) provides. It is not meant to substitute it nor compete with it.

## Requirements
Python libraries: 'bs4', 'selenium', 'webdriver-manager','gtts', 'telegram_send', 'pysimplegui'

Manual install with 
`pip install LIBRARY_NAME`
or run 
`python3 ./libraries/install_dependencies.py`

## RUN
`python3 ./main.py`

## Known issues and future updates
- Installation of the required python packages is manual or via the script mentione above. Future updates will detect missing libraries and install them automatically.
- No cancel button implementation yet. To parse another url simply paste the new one an the thread in the background will pick it up, but the only way to not parse is to close the app



