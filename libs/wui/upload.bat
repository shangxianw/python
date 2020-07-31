@echo off

echo 准备开始！
python setup.py sdist bdist_wheel

echo 输入你的账号密码
python -m twine upload --repository pypi dist/*

echo OK!!
pause