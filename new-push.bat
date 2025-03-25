@echo off
echo Starting clean push...

:: Backup .env
move .env .env.backup 2>nul

:: Remove sensitive files and history
rmdir /S /Q .git
rmdir /S /Q Backend\node_modules
del /F /Q tokens-to-remove.txt
del /F /Q cleanup.txt
del /F /Q exclude.txt

:: Initialize new repository
git init
git checkout -b main

:: Add and commit files
git add .
git commit -m "Clean repository setup"

:: Configure remote and push
git remote add origin https://github.com/Assassin2306/NarcoTrace
git push -f -u origin main

:: Restore .env
move .env.backup .env 2>nul

echo Push complete!
