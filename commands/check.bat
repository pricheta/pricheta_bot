@echo off
set CODE=domain adapters apps

cls
ruff check %CODE% --fix --select I,F401,F841
ruff format %CODE%
ruff check %CODE%
if errorlevel 1 exit /b 1
:: pytest tests --cov=. --cov-report=term-missing:skip-covered