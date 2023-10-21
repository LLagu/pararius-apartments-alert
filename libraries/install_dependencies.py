import subprocess
import sys

def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

def InstallDependencies():
    libraries = ['bs4', 'selenium', 'webdriver-manager','gtts', 'telegram_send']
    for package in libraries:
        install(package)