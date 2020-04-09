from stats import *
import datetime as dt


if __name__ == '__main__':
    days_offset = 180
    curr_date = dt.datetime.now().date()
    start_date = curr_date - dt.timedelta(days=days_offset)
    colors = Color()
    all_commits = get_all_commits("/Users/ruiyewang/Desktop")
    filtered_commits = filter_commits(all_commits, "wokegrdws", start_date)
    date_dict = build_date_dict(filtered_commits, start_date, days_offset)
    list_weekday_dict = build_weekday_dict(date_dict)
    print_figure(list_weekday_dict, start_date)


