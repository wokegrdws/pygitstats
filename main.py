from stats import *


def pygitstats():
    dir_path = input("Provide directory path: ")
    username = input("Your commit username: ")
    days_offset = int(input("How many days you want to check: "))

    print('Checking the past', days_offset, 'contributions for', username, 'in', dir_path)
    curr_date = dt.datetime.now().date()
    start_date = curr_date - dt.timedelta(days=days_offset)
    all_commits = get_all_commits(dir_path)
    filtered_commits = filter_commits(all_commits, username, start_date)
    date_dict = build_date_dict(filtered_commits, start_date, days_offset)
    list_weekday_dict = build_weekday_dict(date_dict)
    print_figure(list_weekday_dict, start_date)


if __name__ == '__main__':
    pygitstats()
