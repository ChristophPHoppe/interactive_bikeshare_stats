import time
import pandas as pd

CITY_DATA = { 'chicago': '/Users/christophhoppe/Desktop/Coding/CSV_Data/chicago.csv',
              'new york city': '/Users/christophhoppe/Desktop/Coding/CSV_Data/new_york_city.csv',
              'washington': '/Users/christophhoppe/Desktop/Coding/CSV_Data/washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, day to analyze and provides a check loop at the end.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print("\nHello! Let\'s explore some US bikeshare data!\n")

    print("Which City do you want to receive information about?\n\nType either \"chicago\", \"washington\" or \"new york city\", or in case you want all to be analyzed, type \"all\".")

    city = input().lower()

    while city not in ["chicago", "new york city", "washington", "all"]:
        print("Something went wrong. Please try again.")
        city = input()

    print("\nWhich months should be considered?\n\nType either a specific month (until june (incl.)), or \"all\", if you want all months to be considered.")

    month = input().lower()

    while month not in ["all", "january", "february", "march", "april", "may", "june"]:
        if month in ["july", "august", "september", "october", "november", "december"]:
            print("Unfortunatly, data is merely available for the months until june. Please try again.")
            month = input().lower()
        else:
            print("Something went wrong. Please try again.")
            month = input().lower()

    print("\nWhich weekday should be included?\n\nType either a specific weekday, or \"all\", if you want all days to be considered.")

    day = input().lower()

    while day not in ["all", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]:
        print("Something went wrong. Please try again.")
        day = input().lower()

    print("\nYou chose to receive information on bikeshare data with the following attributes:\n\nCity: {}\nMonth: {}\nDay: {}\n\nIf this is correct, press enter - if you want to edit your input type \"again\".".format(city, month, day))

    check = input()

    while check != "":
        get_filters()
        break

    print('-'*40)

    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city, or "all" cities to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    if city == "all":
        df_chic = pd.read_csv(CITY_DATA.get("chicago"))
        df_nyc = pd.read_csv(CITY_DATA.get("new york city"))
        df_wash = pd.read_csv(CITY_DATA.get("washington"))

        df = df_chic.append([df_nyc, df_wash])
    else:
        df = pd.read_csv(CITY_DATA[city])

    df["Start Time"] = pd.to_datetime(df["Start Time"])
    df["month"] = df["Start Time"].dt.month
    df["day_of_week"] = df["Start Time"].dt.dayofweek

    if month != "all":
        months = ["january", "february", "march", "april", "may", "june"]
        month = months.index(month) + 1

        df = df[df["month"] == month]
    
    if day != "all":
        days =["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
        day = days.index(day)

        df = df[df["day_of_week"] == day]
    
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    best_month_int = df["month"].mode()[0]
    months = ["january", "february", "march", "april", "may", "june"]
    best_month_str = months[best_month_int - 1]
    print("Most frequent month: {}.".format(best_month_str))

    best_day_int = df["day_of_week"].mode()[0]
    days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
    best_day_str = days[best_day_int]
    print("\nMost frequent day: {}.".format(best_day_str))
    
    best_hour = df["Start Time"].dt.hour.mode()[0]
    print("\nMost frequent start time: {}.".format(best_hour))
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    best_start_station = df["Start Station"].mode()[0]
    print("\nMost frequent start station: {}.".format(best_start_station))

    best_end_station = df["End Station"].mode()[0]
    print("\nMost frequent end station: {}.".format(best_end_station))

    df["Start and End Station"] = df["Start Station"].str.cat(df["End Station"], sep = " - ")
    most_common_combination = df["Start and End Station"].mode()[0]
    print("\nMost frequent combination of start and end station: {}.".format(most_common_combination))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    Tot_travel_time = df["Trip Duration"].sum()
    Tot_travel_time_h = Tot_travel_time/3600
    print("Total travel time: {:,.2f} hours.".format(Tot_travel_time_h))

    mean_travel_time = df["Trip Duration"].mean()
    print("\nAverage travel time: {:,.2f} minutes".format(mean_travel_time/60))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    user_type_series = df["User Type"].value_counts()
    set_stop_user = df["User Type"].nunique()

    for i in range(set_stop_user):
        if user_type_series[i] > 1:
            print("\nCustomers of user type {}: {:,}.".format(user_type_series.index[i], user_type_series[i]))
        else:
            print("\nCustomers of user type {}: {:,}.".format(user_type_series.index[i], user_type_series[i])) 

    if "Gender" in df.columns:
        gender_series = df["Gender"].value_counts()

        for i in range(2):
            print("\n{} customers: {:,}.".format(gender_series.index[i], gender_series[i]))

    else: 
        print("\nUnfortunately, there is no data on gender available for your request.")

    if "Birth Year" in df.columns:
        max_age = df["Birth Year"].max()
        min_age = df["Birth Year"].min()
        most_common_age = df["Birth Year"].mode()[0]

        print("\nBirth year oldest customer: {:.0f}.".format(min_age))
        print("\nBirth year youngest customer: {:.0f}.".format(max_age))
        print("\nMost frequent birth year: {:.0f}.".format(most_common_age))

    else: 
        print("\nUnfortunately, there is no data on birth year available for your request.")

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def raw_data(df):
    """ Displays raw data to the user. On request the user is able to extent the raw data by five lines per repetition. """

    raw_data_request = input("\nDo you want to take a look at the raw data?\n\nPress Enter to display the first five lines or enter \"no\" to continue with descriptive statistics.")

    count = 1
    while raw_data_request == "":
        print(df.head(count*5))
        count += 1
        raw_data_request = input("\nFor additional lines of raw data press Enter. In case you want to continue with descriptive statistcs, enter \"no\".")

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)


        raw_data(df)
        time_stats(df)

        raw_data(df)
        station_stats(df)

        raw_data(df)
        trip_duration_stats(df)

        raw_data(df)
        user_stats(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
