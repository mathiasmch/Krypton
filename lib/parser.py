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


from os import path
from lib.elements import ELEMENTS

################################################################################

def extract_group(file_, group):
    """
    Extract the lines between $"group" and $end (both non-included).

    file_ : GAMESS (US) input file or basis set file from the BSE portal
    group : name of the group to extract (data, ecp, etc.) (case insensitive)
    return : list of right-trimmed lines
    """

    data = list()

    if not path.isfile(file_):
        raise Exception("ERROR: Unable to open file "+file_+".")

    with open(file_) as f:

        read_data = False

        for line in f:
            if read_data:
                if line.strip().lower() == "$end":
                    read_data = False
                else:
                    data.append(line.rstrip())
            else:
                if line.strip().lower() == "$"+group:
                    read_data = True

    return data

################################################################################

def extract_atoms(input_file):
    """
    Extract the list of atoms from the $data group.

    input_file : GAMESS (US) input file
    return : list of trimmed lines
    """

    data = extract_group(input_file, "data")

    if data[1].strip().lower() == "c1":
        index_first_atom = 2
    else:
        index_first_atom = 3

    return data[index_first_atom:len(data)]

################################################################################

def extract_geometry(input_file):
    """
    Extract the coordinates from the list of atoms from the $data group.

    input_file : GAMESS (US) input file
    return : list of list of floats
    """

    geometry = list()

    atoms = extract_atoms(input_file)
    for atom in atoms:
        geometry.append([float(x) for x in atom.split()[-3:]])

    return geometry

################################################################################

def extract_basis_set(basis_set_file):
    """
    Extract the basis set from a GAMESS (US) basis set file.

    basis_set_file : GAMESS (US) input file from the BSE portal
    return : dictionary = list of strings for each atom
             example: {'H':['S 3','1 3.425 0.154','2 0.623 0.535'], 'C': ...}
    """

    basis_set = dict()

    data = extract_group(basis_set_file, "data")

    current_element = ""
    prev_line = ""

    for line in data:

        if prev_line == "":
            current_element = ELEMENTS[line]
            basis_set[current_element] = []

        elif not line:
            current_element = ""

        else:
            basis_set[current_element].append(line)

        prev_line = line

    return basis_set

################################################################################

def extract_ECPs(basis_set_file):
    """
    Extract the ECPs from a GAMESS (US) basis set file.

    basis_set_file : GAMESS (US) input file from the BSE portal
    return : dictionary = list of strings for each atom
             example: {'Ni':['NI-ECP GEN 10 2','...'], 'Fe': ...}
    """

    ECPs = dict()

    ecp = extract_group(basis_set_file, "ecp")

    if ecp:

        element = ""
        for line in ecp:
            maybe_element = line.split('-')[0].strip().lower().title()

            if maybe_element in ELEMENTS.values():
                element = maybe_element
                ECPs[element] = [line]
            else:
                ECPs[element].append(line)

    return ECPs

