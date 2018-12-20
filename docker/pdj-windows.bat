SET NUM=0

:LOOP
SET /A NUM = %NUM% + 1
FOR /f "usebackq" %%G in (`docker ps -q -f "name=pdj-%NUM%"`) DO set PDJID=%%G
IF [%PDJID%] == [] GOTO QUERY
SET PDJID=
GOTO LOOP

:QUERY
set INPUT=
set /P INPUT=Which version of pdia would you like to use? (1=master, 2=2018xval, 3=py3, 0=test): %=%
IF /I "%INPUT%"=="1" GOTO MASTER
IF /I "%INPUT%"=="2" GOTO 2018XVAL
IF /I "%INPUT%"=="3" GOTO PY3
IF /I "%INPUT%"=="0" GOTO TEST
GOTO QUERY

:MASTER
SET PDJTAG=master
GOTO RUN

:2018XVAL
SET PDJTAG=2018xval
GOTO RUN

:PY3
SET PDJTAG=py3
GOTO RUN

:TEST
SET PDJTAG=test
GOTO RUN

:RUN
SET /A PORT = %NUM% + 8887
docker pull pdia/docked-jupyter:%PDJTAG%
docker run -p %PORT%:8888 -h CONTAINER -d -it --rm --name pdj-%NUM%-%PDJTAG% -v "%cd%":/home/jovyan/work pdia/docked-jupyter:%PDJTAG% jupyter notebook --NotebookApp.token='pdia'
timeout /t 5
start http://localhost:%PORT%/?token=pdia
timeout /t -1
docker stop pdj-%NUM%-%PDJTAG%
