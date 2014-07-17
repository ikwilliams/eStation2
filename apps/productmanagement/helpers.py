# -*- coding: utf-8 -*-
#
#	purpose: Dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import

import datetime

from .exceptions import WrongSequence


def find_gaps(filenames, frequency):
    gaps = []
    next_filename = None
    for filename in filenames:
        if not frequency.filename_mask_ok(filename):
            continue
        if not next_filename is None:
            while next_filename < filename:
                gaps.append(next_filename)
                next_filename = frequency.next_filename(next_filename)
            if next_filename != filename:
                raise WrongSequence(filename, next_filename)
        next_filename = frequency.next_filename(filename)
    return gaps


def add_years(date, years=1):
    try:
        return date.replace(year = date.year + years)
    except ValueError:
        # 29 of february return 28 of february
        return date + (datetime.date(date.year + years, 1, 1)
                - datetime.date(date.year, 1, 1)) - datetime.timedelta(days=1)
    

def add_months(date, months=1):
    targetmonth = months + date.month
    try:
        date = date.replace(year=date.year + int((targetmonth - 1)/12), month=((targetmonth - 1)%12 + 1))
    except ValueError:
        # There is an exception if the day of the month we're in does not exist in the target month
        # Go to the FIRST of the month AFTER, then go back one day.
        targetmonth += 1
        date = date.replace(year=date.year + int((targetmonth - 1)/12), month=((targetmonth - 1)%12 + 1), day=1)
        date -= datetime.timedelta(days=1)
    return date


def add_dekads(date, dekads=1):
    dekad = datetime.timedelta(days=10)
    for count_dekad in range(dekads):
        new_date = date + dekad
        if new_date.day == 31:
            new_date += datetime.timedelta(1)
        elif new_date.month != date.month:
            new_date = date - dekad
            new_date = add_months(new_date, 1)
            while new_date.month != date.month:
                new_date -= dekad
            new_date += dekad
        date = new_date
    return date
