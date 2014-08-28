# -*- coding: utf-8 -*-
#
#	purpose: Dataset functions
#	author:  Marco Beri marcoberi@gmail.com
#	date:	 09.07.2014
#

from __future__ import absolute_import

import os
import datetime

from .exceptions import WrongSequence, WrongDateParameter


def cast_to_int(value):
    if isinstance(value, int):
        return value
    try:
        if isinstance(value, float):
            return int(value)
        if isinstance(value, str) or isinstance(value, unicode):
            return int(value.split(".")[0])
    except ValueError:
        pass
    return value


def no_ext(filename):
    return os.path.splitext(filename)[0]


def get_ext(filename):
    try:
        return os.path.splitext(filename)[1]
    except IndexError:
        return ""


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


def add_xkads(date, xkads, days=10):
    delta = datetime.timedelta(days)
    for count_dekad in range(xkads):
        new_date = date + delta
        if new_date.day == 31:
            new_date += datetime.timedelta(1)
        elif new_date.month != date.month:
            new_date = date - delta
            new_date = add_months(new_date, 1)
            while new_date.month != date.month:
                new_date -= delta
            new_date += delta
        date = new_date
    return date


def add_dekads(date, dekads=1):
    return add_xkads(date, dekads, 10)


def add_pentads(date, pentads=1):
    return add_xkads(date, pentads, 5)


def add_days(date, period, days):
    delta = datetime.timedelta(days)
    for count_dekad in range(period):
        new_date = date + delta
        if new_date.year > date.year:
            new_date = datetime.date(new_date.year, 1, 1)
        date = new_date
    return date


class INTERVAL_TYPE:
    PRESENT = 'present'
    MISSING = 'missing'
    PERMANENT_MISSING = 'permanent-missing'


def find_gaps(unsorted_filenames, frequency, only_intervals=False, from_date=None, to_date=None):
    for date_parameter in (from_date, to_date):
        if date_parameter and not frequency.check_date(date_parameter):
            raise WrongDateParameter(date_parameter, frequency.dateformat)
    gaps = []
    interval = []
    intervals = []
    next_filename = last_filename = None
    last_filename_added = False
    filenames = sorted(no_ext(f) for f in unsorted_filenames if not f is None)
    original_filenames = dict((no_ext(f), f) for f in unsorted_filenames if not f is None)
    original_ext = get_ext(unsorted_filenames[0]) if unsorted_filenames else ""
    mapset = frequency.get_mapset((filenames or [''])[0])
    if not from_date is None:
        next_filename = frequency.format_filename(from_date, mapset)
    if not to_date is None:
        last_filename = frequency.format_filename(to_date, mapset)
        if (not filenames) or (filenames[-1] < last_filename):
            last_filename_added = True
            filenames.append(last_filename)
    for filename in filenames:
        if not next_filename is None:
            while next_filename < filename or (last_filename_added and next_filename == last_filename):
                if len(interval) == 0:
                    interval = [next_filename + original_ext, next_filename + original_ext, INTERVAL_TYPE.PRESENT]
                else:
                    interval[1] = next_filename + original_ext
                gaps.append(next_filename + original_ext)
                next_filename = frequency.next_filename(next_filename)
            if interval:
                intervals.append(interval)
                interval = []
            if next_filename != filename and filename != last_filename:
                original = original_filenames[filename]
                raise WrongSequence(original, next_filename + get_ext(original))
        else:
            interval
        next_filename = frequency.next_filename(filename)
    if only_intervals:
        return intervals
    return gaps


def _find_gaps(unsorted_filenames, frequency, only_intervals=False, from_date=None, to_date=None):
    for date_parameter in (from_date, to_date):
        if date_parameter and not frequency.check_date(date_parameter):
            raise WrongDateParameter(date_parameter, frequency.dateformat)
    gaps = []
    interval = []
    intervals = []
    next_filename = last_filename = None
    last_filename_added = False
    filenames = sorted(no_ext(f) for f in unsorted_filenames if not f is None)
    original_filenames = dict((no_ext(f), f) for f in unsorted_filenames if not f is None)
    original_ext = get_ext(unsorted_filenames[0]) if unsorted_filenames else ""
    mapset = frequency.get_mapset((filenames or [''])[0])
    if not from_date is None:
        next_filename = frequency.format_filename(from_date, mapset)
    if not to_date is None:
        last_filename = frequency.format_filename(to_date, mapset)
        if (not filenames) or (filenames[-1] < last_filename):
            last_filename_added = True
            filenames.append(last_filename)
    for filename in filenames:
        if not next_filename is None:
            while next_filename < filename or (last_filename_added and next_filename == last_filename):
                if len(interval) == 0:
                    interval = [next_filename + original_ext, next_filename + original_ext]
                else:
                    interval[1] = next_filename + original_ext
                gaps.append(next_filename + original_ext)
                next_filename = frequency.next_filename(next_filename)
            if interval:
                intervals.append(interval)
                interval = []
            if next_filename != filename and filename != last_filename:
                original = original_filenames[filename]
                raise WrongSequence(original, next_filename + get_ext(original))
        else:
            interval
        next_filename = frequency.next_filename(filename)
    if only_intervals:
        return intervals
    return gaps


def add_years(date, years=1):
    try:
        return date.replace(year = date.year + years)
    except ValueError:
        # 29 of february return 28 of february
        return date + (datetime.date(date.year + years, 1, 1)
                - datetime.date(date.year, 1, 1)) - datetime.timedelta(days=1)
    

