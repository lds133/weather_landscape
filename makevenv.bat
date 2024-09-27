set PYTHONEXE=python 


rmdir .venv /s /q
%PYTHONEXE% -m venv .venv
call .venv\Scripts\activate
call pip install -r requirements.txt
xcopy secrets.py.example secrets.py
deactivate