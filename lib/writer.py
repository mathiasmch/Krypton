#! /usr/bin/env python3.4
# -*- coding:utf-8 -*-
#
# Krypton - A little tool for GAMESS (US) users
#
# Copyright (C) 2012-20.. Mathias M.
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.


from os import listdir
from lib.config import *
from lib.basisset import load_basis_set

################################################################################

def insert_basis_set(input_file, output_file, bsid):
    """
    Write the GAMESS (US) input file output_file by adding the basis set bsid
    to the input_file.

    input_file : GAMESS (US) input file
    output_file : name of the file to create
    bsid : ID of the basis set to insert
    """

    basis_set = load_basis_set(bsid)

    with open(output_file, "w") as of:

        read_data = False
        read_atoms = False
        prev_line = "..."

        with open(input_file) as f:
            for line in f:

                if read_data:

                    if line.strip().lower() == "$end":
                        of.write(line)
                        read_data = False

                    else:

                        if prev_line.strip() == "C1" or prev_line.strip() == "":
                                read_atoms = True

                        if read_atoms:

                            line = line.strip()
                            element = line.split()[0]

                            if element in basis_set:

                                of.write(line+"\n")

                                coeffs = basis_set[element]
                                for coeff in coeffs:
                                    of.write(coeff+"\n")

                                of.write("\n")

                            else:
                                raise Exception("ERROR: Element "+element+" is not available this basis set.")

                        else:
                            of.write(line)

                else:

                    of.write(line)

                    if line.strip().lower() == "$data":
                        read_data = True

                prev_line = line

