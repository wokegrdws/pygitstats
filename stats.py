import collections

from scan import *
from git import Repo
import datetime as dt


class Color(object):
    reset = '\x1b[0m'
    red = '\x1b[30;41m'
    green = '\x1b[30;42m'
    yellow = '\x1b[30;43m'
    blue = '\x1b[30;44m'
    magenta = '\x1b[30;45m'
    cyan = '\x1b[30;46m'
    white = '\x1b[30;47m'


# get commits from the given repo
def _get_commits(repo_path):
    try:
        repo = Repo(repo_path)
        all_commits = list(repo.iter_commits())
        return all_commits
    except:
        return []


# get all commits from the given dir_name
def get_all_commits(dir_name):
    all_commits = list()
    list_git_dir = get_git_dir(dir_name)
    try:
        for file_name in list_git_dir:
            all_commits = all_commits + _get_commits(file_name)
    except:
        pass
    return all_commits


# find commits that match the author, and after start_date
def filter_commits(list_commits, author, start_date):
    new_list = list()
    for commit in list_commits:
        try:
            commit_author = str(commit.author)
            commit_date = dt.datetime.strptime(str(commit.committed_datetime.date()), "%Y-%m-%d").date()
            if (commit_author == author or commit.committer == author) and commit_date >= start_date:
                new_list.append(commit)
        except:
            pass
    return new_list


# count the number of commits for each date
def build_date_dict(list_commits, start_date, days_offset):
    date_dict = {}

    # fill in date_dict with all 0
    for i in range(days_offset + 1):
        date_dict[start_date + dt.timedelta(days=i)] = 0

    for commit in list_commits:
        try:
            date = commit.committed_datetime.date()
            if date in date_dict:
                date_dict.update({date: date_dict.get(date) + 1})
            else:
                date_dict[date] = 1
        except:
            pass
    # use OrderedDict
    date_dict = collections.OrderedDict(sorted(date_dict.items()))
    return date_dict


def build_weekday_dict(date_dict):
    sunday_dict = {}
    monday_dict = {}
    tuesday_dict = {}
    wednesday_dict = {}
    thurday_dict = {}
    friday_dict = {}
    saturday_dict = {}

    for key in date_dict.keys():
        weekday = key.weekday()
        if weekday == 0:
            monday_dict[key] = date_dict[key]
        elif weekday == 1:
            tuesday_dict[key] = date_dict[key]
        elif weekday == 2:
            wednesday_dict[key] = date_dict[key]
        elif weekday == 3:
            thurday_dict[key] = date_dict[key]
        elif weekday == 4:
            friday_dict[key] = date_dict[key]
        elif weekday == 5:
            saturday_dict[key] = date_dict[key]
        elif weekday == 6:
            sunday_dict[key] = date_dict[key]

    list_weekday_dict = [sunday_dict, monday_dict, tuesday_dict,
                         wednesday_dict, thurday_dict, friday_dict, saturday_dict]
    # sort each weekday_dict
    for i in range(len(list_weekday_dict)):
        weekday_dict = list_weekday_dict[i]  # start from sunday
        # use OrderedDict
        list_weekday_dict[i] = collections.OrderedDict(sorted(weekday_dict.items()))

    return list_weekday_dict


def _print_cell(value):
    colors = Color()
    if value == 0:
        color = colors.white
    elif 0 < value <= 3:
        color = colors.green
    elif 3 < value <= 6:
        color = colors.blue
    elif 6 < value <= 9:
        color = colors.yellow
    elif 9 < value <= 12:
        color = colors.magenta
    else:
        color = colors.cyan
    print(color + ' ' + str(value) + ' ' + colors.reset, end='')
    # print(colors.white + ' ' + str(value) + ' ' + colors.reset, end='')


def print_figure(list_weekday_dict, start_date):

    for i in range(len(list_weekday_dict)):
        weekday_dict = list_weekday_dict[i]  # start from sunday
        if i == 0:
            print('Sun', end='')
        elif i == 1:
            print('Mon', end='')
        elif i == 2:
            print('Tue', end='')
        elif i == 3:
            print('Wed', end='')
        elif i == 4:
            print('Thu', end='')
        elif i == 5:
            print('Fri', end='')
        elif i == 6:
            print('Sat', end='')

        first_day = list(weekday_dict.keys())[0]
        if first_day > start_date and (first_day.weekday()+1) % 7 < (start_date.weekday()+1) % 7:
            print('   ', end='')

        for key in weekday_dict.keys():
            _print_cell(weekday_dict[key])
        # move to next line
        print('\r')  # if use print(''), might have a problem depending on the terminal
