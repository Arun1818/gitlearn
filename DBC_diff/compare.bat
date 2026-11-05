@echo off
setlocal EnableDelayedExpansion

set "FROM_FILE=%~1"
set "TO_FILE=%~2"

call :GetVersion "%~n1" FROM_VER
call :GetVersion "%~n2" TO_VER

set "OUT_NAME=diff_bw_%FROM_VER%_to_%TO_VER%"

echo Comparing:
echo   From: %FROM_FILE%
echo   To  : %TO_FILE%
echo Output: %OUT_NAME%

python dbcdiff.py -f "%FROM_FILE%" -t "%TO_FILE%" -r html,json -n "%OUT_NAME%"

goto :eof

:GetVersion
set "name=%~1"

for %%a in (%name:_= %) do (
    set "tok=%%a"

    rem Version like v25.05
    if /i "!tok:~0,1!"=="v" (
        set "%~2=!tok:~1!"
        exit /b
    )

    rem Version like 4.3.0
    echo !tok! | findstr /r "^[0-9][0-9\.]*$" >nul
    if not errorlevel 1 (
        set "%~2=!tok!"
        exit /b
    )
)

set "%~2=UNKNOWN"
exit /b
``