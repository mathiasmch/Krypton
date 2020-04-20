# Krypton 0.1

## A tool for GAMESS (US) users

Krypton is tool that helps creating GAMESS (US) input files with any basis set downloaded from the [EMSL Basis Set Exchange](https://bse.pnl.gov/bse/portal) portal.

### Requirements:

- Linux
- Python 3

### How to install it:

    chmod +x krypton.py

### How to use it:

To request help:

    ./krypton.py --help
    ./krypton.py add --help
    ./krypton.py insert --help

To add a basis set to the internal database:

    ./krypton.py add STO-3G examples/STO-3G_H_C.txt
    ./krypton.py add STO-3G examples/STO-3G_H_C_N_O.txt

To list the available basis sets:

    ./krypton.py basissets

To insert a basis set into an input file:

    ./krypton.py insert STO-3G examples/methane.inp examples/methane_STO-3G.inp
    ./krypton.py insert STO-3G examples/water.inp examples/water_STO-3G.inp

