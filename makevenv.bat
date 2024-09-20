set PYTHONEXE=python 


rmdir .venv /s /q
%PYTHONEXE% -m venv .venv
call .venv\Scripts\activate
call pip install -r requirements.txt
deactivate