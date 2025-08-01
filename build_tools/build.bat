@REM A convenience script for compiling Task Tracker 1.0 
@REM into an executable on Windows.
@REM July 2, 2025.


pyinstaller cli.py ^
    --noconsole ^
    --onefile ^
    --windowed ^
    --add-data "src/task_tracker/images/*;task_tracker/images" ^
    --name "Task Tracker 1.0" ^
    --icon timer.ico ^
    --log-level WARN ^
    --noconfirm ^
    --clean
