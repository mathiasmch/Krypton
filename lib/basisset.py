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


from os import listdir, path, makedirs
from lib.config import *
from lib.parser import extract_basis_set, extract_ECPs

################################################################################

def add_basis_set(bsid, basis_set_file):
    """
    Add the basis set of a basis set file from the BSE portal into the folder
    used as database.

    bsid : ID to use for the basis set (STO-3G, 6-31G, etc.)
    basis_set_file : GAMESS (US) input file from the BSE portal
    """

    basis_set = extract_basis_set(basis_set_file)
    ECPs = extract_ECPs(basis_set_file)

    elements = list()
    if bsid in listdir(DB):
        elements = get_elements(bsid)
    else:
        makedirs(DB+"/"+bsid)

    for element, coeffs in basis_set.items():
        if element not in elements:
            with open(DB+"/"+bsid+"/"+element+".txt", "w") as f:
                for coeff in coeffs:
                    f.write(coeff+"\n")

    if ECPs:
        if "ECP" not in listdir(DB+"/"+bsid):
            makedirs(DB+"/"+bsid+"/ECP")

        elements = get_elements(bsid, True)

        for element, coeffs in ECPs.items():
            if element not in elements:
                with open(DB+"/"+bsid+"/ECP/"+element+".txt", "w") as f:
                    for coeff in coeffs:
                        f.write(coeff+"\n")

################################################################################

def load_basis_set(bsid):
    """
    Extract the basis set from the database.

    bsid : ID of the basis set
    return : dictionary = list of strings for each atom
             example: {'H':['S 3','1 3.425 0.154','2 0.623 0.535'], 'C': ...}
    """

    basis_set = dict()

    if not path.isdir(DB):
        raise Exception("ERROR: There is no database.")

    if bsid not in listdir(DB):
        raise Exception("ERROR: Basis set "+bsid+" does not exist.")

    for element_file in listdir(DB+"/"+bsid):
        if element_file != "ECP":

            element = element_file.split(".")[0]

            with open(DB+"/"+bsid+"/"+element_file) as f:
                basis_set[element] = []
                for line in f:
                    basis_set[element].append(line.rstrip())

    return basis_set

################################################################################

def get_elements(bsid, ECP=False):
    """
    Return the elements available in the database for the basis set bsid.

    bsid : ID of the basis set
    return : list of elements
    """

    elements = list()

    if bsid not in listdir(DB):
        raise Exception("ERROR: Basis set "+bsid+" does not exist.")

    path = DB+"/"+bsid
    if ECP:
        path += "/ECP"

    for element in listdir(path):
        if element.endswith(".txt"):
            elements.append(element.split(".")[0])

    return elements

################################################################################

def list_basis_sets():
    """
    Print the available basis sets in the database and their atoms.
    """

    if not path.isdir(DB):
        raise Exception("ERROR: There is no database.")

    for bsid in listdir(DB):
        line = bsid + " : "
        for elements in get_elements(bsid):
            line += elements
            line += " "

        if "ECP" in listdir(DB+"/"+bsid):
            line += "(ECP :"
            ECPs = get_elements(bsid, True)
            for ECP in ECPs:
                line += " "
                line += ECP
            line += ")"

        print(line)

