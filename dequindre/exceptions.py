# -*- coding: utf-8 -*-
"""Exceptions that are unique to dequindre.
"""
class CyclicGraphError(Exception):
    """Dequindre will generate an infinite schedule given a cyclic graph"""


class EarlyAbortError(Exception):
    """Used in conjunction with Dequindre.run_tasks() for error handling"""
