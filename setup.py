import cx_Freeze

executables = [cx_Freeze.Executable(script="main.py", icon="space.png")]

cx_Freeze.setup(
    name="Space Marker",
    version = "1.0",
    options={"build_exe":
        {"packages":
            ["pygame", "tkinter", "os"],"include_files":["bg.jpg", "estrela.png", "nave.png", "Space_Machine_Power.mp3", "Space_sound.mp3", "space.ico", "space.png"]}},
    executables = executables
)