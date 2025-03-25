@echo off
echo Starting clean push...

:: Ensure .env exists
if not exist ".env" (
    copy .env.example .env
    echo Created .env from example
)

:: Remove old Git history
rmdir /S /Q .git 2>nul

:: Initialize new repository
git init
git checkout -b main

:: Add all files
git add .

:: Create commit
git commit -m "Clean repository initialization"

:: Add remote and push
git remote add origin https://github.com/Assassin2306/NarcoTrace
git push -f -u origin main

echo Push complete!
pause
