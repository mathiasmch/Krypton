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


from argparse import ArgumentParser
from os import path, makedirs
from lib.config import *
from lib.basisset import add_basis_set, list_basis_sets
from lib.writer import insert_basis_set

################################################################################

p = ArgumentParser(
            prog="krypton",
            description="Krypton is little tool that helps creating GAMESS " 
                        "(US) input files with any basis set downloaded from "
                        "the EMSL Basis Set Exchange portal.")

sub_p = p.add_subparsers(dest="subparser_name")

add_p = sub_p.add_parser("add", help="add a basis set to the database")
add_p.add_argument("basis_set", type=str, help="name of the basis set")
add_p.add_argument("file", type=str, help="file containing the basis set to add")

basissets_p = sub_p.add_parser("basissets", help="list available basis sets")

insert_p = sub_p.add_parser("insert", help="insert a basis set into an input file")
insert_p.add_argument("basis_set", type=str, help="name of the basis set")
insert_p.add_argument("input", type=str, help="input file in the GAMESS (US) format")
insert_p.add_argument("output", type=str, help="output file")

args = p.parse_args()

################################################################################

try:

    if args.subparser_name == "add":
        if not path.isdir(DB):
            makedirs(DB)
        add_basis_set(args.basis_set, args.file)

    elif args.subparser_name == "basissets":
        list_basis_sets()

    elif args.subparser_name == "insert":
        insert_basis_set(args.input, args.output, args.basis_set)

except Exception as exception:
    print(exception)

