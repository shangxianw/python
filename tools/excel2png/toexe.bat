@echo off

rd /s /q __pycache__
rd /s /q build
rd /s /q dist
del /f /s /q index.spec
del /f /s /q index.exe

pyinstaller -F -w index.py