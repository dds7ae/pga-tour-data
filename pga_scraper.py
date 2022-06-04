import requests  # Request module
import pandas as pd  # Data Wrangling
from bs4 import BeautifulSoup  # Web scraping module
import time


def get_headers(soup):
    '''This function get's the column names to use for the data frame.'''
    # First header is always going to be the one we care about most for that page
    headers = [soup.find(class_="col-stat").get_text()]

    # Get rounds header
    if soup.find_all(class_="rounds hidden-small hidden-medium"):
        rounds = soup.find_all(class_="rounds hidden-small hidden-medium")[0].get_text()
        headers.append(rounds)

    # Get other headers
    stat_headers = soup.find_all(class_="col-stat hidden-small hidden-medium")
    for header in stat_headers:
        headers.append(header.get_text())

    return headers


def get_headers_labels(soup):
    '''This function get's the column names to use for the data frame.'''
    headers = [soup.find(class_="col-stat").get_text()]

    return headers


# Get Players
def get_players(soup):
    '''This function takes the beautiful soup created and uses it to gather player names from the specified stats page.'''
    # This works perfectly fine as of now.
    player_list = []

    # Get player as html tags
    players = soup.select('td a')[1:]  # Use 1 because first line of all tables is not useful.
    # Loop through list
    for player in players:
        player_list.append(player.get_text())

    return player_list


##Get Stats
def get_stats(soup, column, categories):
    '''This function takes the soup created before,
    the column of the category we care about (count from 1 from left to column x), and
    the number of other categories on the page (count from right of player to end not including column x).'''
    # Step 1: Find the other metrics on the page
    stats = soup.find_all(class_="hidden-small hidden-medium")[1:]  # First column is garbage
    stat_list = []
    for i in range(0, len(stats) - categories + 1, categories):
        temp_list = []
        for j in range(categories):
            temp_list.append(stats[i + j].get_text())
        stat_list.append(temp_list)

    # Step 2: Find the metric we care about
    rows = soup.find_all("tr", id=lambda value: value and value.startswith("playerStatsRow"))
    for i, row in enumerate(rows):
        stat_list[i].insert(0, row.find_all_next("td")[column].get_text().replace(",", ""))
    return stat_list


def get_labels(soup, column):
    '''This function takes the soup created before,
    the column of the category we care about (count from 1 from left to column x excluding player name), and
    the number of other categories on the page (count from right of player name excluding column x).'''
    stat_list = []
    rows = soup.find_all("tr", id=lambda value: value and value.startswith("playerStatsRow"))
    for row in rows:
        stat_list.append([row.find_all_next("td")[column].get_text()])
    return stat_list


def stats_dict(players, stats):
    '''This function takes two lists, players and stats,
    and creates a dictionary with the player being the key
    and the stats as the vales (as a list)'''

    # initialize player dictionary
    player_dict = {}

    # Loop through player list
    for i, player in enumerate(players):
        player_dict[player] = stats[i]

    return player_dict


##Mega function
def make_dataframe(url, column, categories):
    # Create soup object from url.
    response = requests.get(url)
    time.sleep(5)
    text = response.text
    soup = BeautifulSoup(text, 'lxml')

    # 1. Get Headers
    headers = get_headers(soup)
    print(headers)
    # 2. Get Players
    players = get_players(soup)
    print(players)
    # 3. Get Stats
    stats = get_stats(soup, column, categories)
    print(stats)
    # 4. Make stats dictionary.
    stats_dictionary = stats_dict(players, stats)
    print(stats_dictionary)
    # Make dataframe
    frame = pd.DataFrame(stats_dictionary, index=headers).T
    print(frame)
    # Reset index
    frame = frame.reset_index()

    # For each Dataframe, change index column to 'NAME'
    frame = frame.rename(index=str, columns={'index': 'NAME'})
    return frame


def make_dataframe_label(url, column):
    # Create soup object from url.
    response = requests.get(url)
    time.sleep(5)
    text = response.text
    soup = BeautifulSoup(text, 'lxml')

    # 1. Get Headers
    headers = get_headers_labels(soup)
    print(headers)
    # 2. Get Players
    players = get_players(soup)
    print(players)
    # 3. Get Stats
    stats = get_labels(soup, column)
    print(stats)
    # 4. Make stats dictionary.
    stats_dictionary = stats_dict(players, stats)
    print(stats_dictionary)
    # Make dataframe
    frame = pd.DataFrame(stats_dictionary, index=headers).T
    print(frame)
    # Reset index
    frame = frame.reset_index()

    # For each Dataframe, change index column to 'NAME'
    frame = frame.rename(index=str, columns={'index': 'NAME'})
    return frame


# Apparently US open 2020 was held in 2021
# and FedEx cups points are wack for 2019, and 2021.
years = ['2016', '2017', '2018', '2019', '2021']


for year in years:
    # Fedex cup points
    # fcp = make_dataframe("https://www.pgatour.com/stats/stat.02671.y{}.html".format(year), 4, 5)[['NAME', 'POINTS']]

    # Top 10's and wins
    top10 = make_dataframe("https://www.pgatour.com/stats/stat.138.y{}.html".format(year), 3, 3)[
        ['NAME', 'TOP 10', '1ST']]

    # Scoring statistics, keep rounds from this page as
    # it most accurately reflects total rounds player completed in season.
    scoring = make_dataframe("https://www.pgatour.com/stats/stat.120.y{}.html".format(year), 4, 4)[
        ['NAME', 'ROUNDS', 'AVG']]
    scoring = scoring.rename(columns={'AVG': 'SCORING'})

    # Driving Distance
    drivedistance = make_dataframe("https://www.pgatour.com/stats/stat.101.y{}.html".format(year), 4, 3)[
        ['NAME', 'AVG.']]
    # Rename Columns
    drivedistance = drivedistance.rename(columns={'AVG.': 'DRIVE_DISTANCE'})

    # Driving Accuracy
    driveacc = make_dataframe("https://www.pgatour.com/stats/stat.102.y{}.html".format(year), 4, 3)[['NAME', '%']]
    # Change column name from % to FWY %
    driveacc = driveacc.rename(columns={'%': "FWY_%"})

    # Greens in Regulation.
    gir = make_dataframe("https://www.pgatour.com/stats/stat.103.y{}.html".format(year), 4, 4)[['NAME', '%']]
    # Change column name from % to GIR %
    gir = gir.rename(columns={'%': "GIR_%"})

    # Strokes gained tee to green
    sg_teetogreen = make_dataframe("https://www.pgatour.com/stats/stat.02674.y{}.html".format(year), 4, 5)[
        ['NAME', 'AVERAGE']]
    # Change name of average column
    sg_teetogreen = sg_teetogreen.rename(columns={'AVERAGE': 'SG_TTG'})

    # Strokes gained total
    sg_total = make_dataframe("https://www.pgatour.com/stats/stat.02675.y{}.html".format(year), 4, 5)[
        ['NAME', 'AVERAGE']]
    sg_total = sg_total.rename(columns={'AVERAGE': 'SG_T'})

    # Strokes gained putting
    sg_putting = make_dataframe("https://www.pgatour.com/stats/stat.02564.y{}.html".format(year), 4, 3)[
        ['NAME', 'AVERAGE']]
    # Change name of average column
    sg_putting = sg_putting.rename(columns={'AVERAGE': 'SG_P'})

    scrambling = make_dataframe("https://www.pgatour.com/stats/stat.130.y{}.html".format(year), 4, 3)[
        ['NAME', '%', 'PAR OR BETTER', 'MISSED GIR']]
    scrambling = scrambling.rename(columns={'%': 'SCRAMBLING_P'})

    # What's ML without labels
    us_open_ranking = make_dataframe_label("https://www.pgatour.com/stats/stat.138.y{}.eoff.t026.html".format(year), 3)[
        ['NAME', 'TOP 10']]
    us_open_ranking = us_open_ranking.rename(columns={'TOP 10': 'US_OPEN_TOP_10'})

    # Get Dataframes into list.
    data_frames = [drivedistance, driveacc, gir, sg_putting, sg_teetogreen, sg_total, scrambling, us_open_ranking]

    # Merge all Dataframes together
    df_one = pd.DataFrame()
    df_one = scoring
    for df in data_frames:
        df_one = pd.merge(df_one, df, on='NAME')

    # merge fex ex cup points
    # df_one = pd.merge(df_one, fcp, how='outer', on='NAME')
    # Merge top 10's
    df_one = pd.merge(df_one, top10, how='outer', on='NAME')


    # Only get people who's scoring average isn't null.
    df_one = df_one.loc[df_one['SCORING'].isnull() == False]

    # Add year column
    df_one['Year'] = year

    # Concat dataframe to overall dataframe
    if year == '2016':
        df_total = pd.DataFrame()
        df_total = pd.concat([df_total, df_one], axis=0)
    else:
        df_total = pd.concat([df_total, df_one], axis=0)

    df_total.to_csv("pga_tour_data.csv")
