@echo off
set CODE=apps

cls
ruff format %CODE%
ruff check %CODE%
mypy %CODE%
if errorlevel 1 exit /b 1
:: pytest tests --cov=. --cov-report=term-missing:skip-covered