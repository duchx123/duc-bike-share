import calendar
import time

import pandas as pd
# refactor 1
# refactor 2
CITY_DATA = {'chicago': 'chicago.csv',
             'new york city': 'new_york_city.csv',
             'washington': 'washington.csv'}
listMonthOfYear = {'January', 'February', 'March', 'April', 'May', 'June'}
listDayOfWeek = {
    "Monday",
    "Tuesday",
    "Wednesday",
    "Thursday",
    "Friday",
    "Saturday",
    "Sunday"
}


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    print('-' * 10)
    count_loop_city = 0
    while True:
        if count_loop_city == 0:
            city = input(
                'Which city do you want to see data for, Chicago, New York or Washington? Please enter below for me:\n')
        else:
            city = input(
                'Input does not exist. '
                'Please enter a valid city name (Chicago, New York, or Washington) below for me:\n')
        print('You have entered the value: {}'.format(city))
        city = city.strip().lower()
        if city in CITY_DATA:
            print('Input  has been recorded. Processing...')
            break
        count_loop_city += 1

    # get user input for month (all, january, february, ... , june)
    print('-' * 10)
    count_loop_month = 0
    while True:
        if count_loop_month == 0:
            month = input(
                'Which month do you want to see data for? Please enter month from January to June (or All):\n')
        else:
            month = input(
                'Input does not exist. Please enter a valid month (January to June or All):\n')
        print('You have entered the value: {}'.format(month))
        month = month.strip().capitalize()
        if month in listMonthOfYear or month == 'All':
            print('Input  has been recorded. Processing...')
            break
        count_loop_month += 1

    # get user input for day of week (all, monday, tuesday, ... sunday)
    count_loop_day = 0
    while True:
        if count_loop_day == 0:
            day = input(
                'Which day of week do you want to see data for? Please enter day below for me (or All):\n')
        else:
            day = input(
                'Input does not exist. Please enter a valid day (or All):\n')
        print('You have entered the value: {}'.format(day))
        day = day.strip().capitalize()
        if day in listDayOfWeek or day == 'All':
            print('Input  has been recorded. Processing...')
            break
        count_loop_day += 1
    print('-' * 40)
    return city, month, day


def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    print("Load DataFrame for: city = {}, month = {}, day of week = {}".format(city, month, day))
    filename = CITY_DATA[city]
    data = pd.read_csv(filename)
    data["Start Time"] = pd.to_datetime(data["Start Time"])

    """Filter data by month and day."""
    if month != "All":
        data = data[data["Start Time"].dt.strftime('%B') == month]
        print("Filtered data with month: {}.\n".format(month))

    if day != "All":
        data = data[data["Start Time"].dt.strftime('%A') == day]
        print("Filtered data with day of week: {}.\n".format(day))
    df = pd.DataFrame(data)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    epoch_start_time = time.time()
    # display the most common month
    df["Month"] = df["Start Time"].dt.month
    common_month_numeric = df["Month"].mode().iloc[0]
    common_month = calendar.month_name[common_month_numeric]
    print("The most common month:", common_month)

    # display the most common day of week
    df["DOW"] = df["Start Time"].dt.dayofweek
    common_dow_numeric = df["DOW"].mode().iloc[0]
    common_dow = calendar.day_name[common_dow_numeric]
    print("The most common day of week:", common_dow)

    # display the most common start hour
    df["Hour"] = df["Start Time"].dt.hour
    common_hour = df["Hour"].mode().iloc[0]
    print("The most common hour:", common_hour)

    epoch_end_time = time.time()
    print("\nThis took {} seconds.".format((epoch_end_time - epoch_start_time)))
    print('-' * 40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    epoch_start_time = time.time()

    # display most commonly used start station
    common_start = df["Start Station"].mode().iloc[0]
    print("The most commonly used start station:", common_start)
    # display most commonly used end station
    common_end = df["End Station"].mode().iloc[0]
    print("The most commonly used end station:", common_end)
    # display most frequent combination of start station and end station trip
    group_combination = df.groupby(['Start Station', 'End Station']).size().reset_index(name='count')
    most_frequent = group_combination.loc[group_combination['count'].idxmax()]
    print("The Most frequent combination: from {} to {}".format(most_frequent['Start Station'],
                                                                most_frequent['End Station']))

    epoch_end_time = time.time()
    print("\nThis took {} seconds.".format((epoch_end_time - epoch_start_time)))
    print('-' * 40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    epoch_start_time = time.time()

    # display total travel time
    total_time = df['Trip Duration'].sum()
    print("Total travel time by seconds:", total_time)

    # display mean travel time
    mean_time = df['Trip Duration'].mean()
    print("Mean travel time by seconds:", mean_time)

    epoch_end_time = time.time()
    print("\nThis took {} seconds.".format((epoch_end_time - epoch_start_time)))
    print('-' * 40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    epoch_start_time = time.time()

    # Display counts of user types
    count_user_types = df["User Type"].value_counts()
    print("Counts of user types:\n", count_user_types)

    # Display counts of gender
    if "Gender" in df.columns:
        count_user_gender = df["Gender"].value_counts()
        print("Counts of user gender:\n", count_user_gender)

    # Display earliest, most recent, and most common year of birth
    if "Birth Year" in df.columns:
        earliest_birth = int(df["Birth Year"].min())
        print("The earliest year of birth:", earliest_birth)

        recent_birth = int(df["Birth Year"].max())
        print("The recent year of birth:", recent_birth)

        common_birth = int(df["Birth Year"].mode().iloc[0])
        print("Most common year of birth:", common_birth)

    epoch_end_time = time.time()
    print("\nThis took {} seconds.".format((epoch_end_time - epoch_start_time)))
    print('-' * 40)


def display_data(df):
    view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n').lower()
    start_loc = 0
    while view_data == 'yes' and start_loc + 5 < df.shape[0]:
        print(df.iloc[start_loc:start_loc + 5])
        start_loc += 5
        view_data = input("Do you wish to continue?: ").lower()

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
        display_data(df)
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
    main()
