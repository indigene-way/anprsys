"""Fichier d'installation de notre script salut.py."""

from cx_Freeze import setup, Executable

# On appelle la fonction setup
setup(
    name = "ANPR Sys.",
    version = "1.0.0",
    description = "ANPR Sys permet la capture et la reconnaissance de matricules, projet développé comme chapitre supplémentaire du mémoir de fin d'étude 2020-2021 G.Halim...",
    executables = [Executable("AnprGUI.py")]
)