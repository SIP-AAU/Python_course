#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Simple introduction script"""


def say_hello(name=None):
    """Print a greeting to the user"""
    if not name:
        name = raw_input("Please enter your name: ")
    print "Hello ", name
    print "Hello (again) %s" % (name)
    print "Hello (and again) {name}".format(name=name)


if __name__ == "__main__":
    say_hello()
