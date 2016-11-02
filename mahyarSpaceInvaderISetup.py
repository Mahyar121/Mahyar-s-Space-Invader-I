import cx_Freeze

executables = [cx_Freeze.Executable("mahyarSpaceInvaderI.py", icon="player.ico")]

cx_Freeze.setup(
    name = "Mahyar's Space Invader I",
    options={"build_exe":{"packages":["pygame"],
                          "include_files":["e1_0.png","e1_1.png","e2_0.png","e2_1.png","e3_0.png","e3_1.png","game_font.ttf","player.png"]}},

    description ="Mahyar's Space Invader I Game",
    executables = executables

)