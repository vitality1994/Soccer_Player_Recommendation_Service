#%% import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import time
import json
from fake_headers import Headers
import argparse
from datetime import datetime

import sys, os

import warnings
warnings.filterwarnings("ignore")

# Selenium settings ----------------------------
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--window-size=1920,1080')
options.add_argument("--disable-gpu")

header = Headers(
    browser="chrome",  # Generate only Chrome UA
    os="win",  # Generate only Windows platform
    headers=False # generate misc headers
)
customUserAgent = header.generate()['User-Agent']

options.add_argument(f"user-agent={customUserAgent}")
# ----------------------------------------------

#%% Run web scraping 

website = 'https:/1xbet.whoscored.com'
path = '/Users/jooyong/Downloads/chromedriver-mac-arm64/chromedriver'

driver = webdriver.Chrome(path, chrome_options=options)
driver.implicitly_wait(20)

driver.get(website)

# league urls
league_urls_num_matchweeks = {'//*[@id="popular-tournaments-list"]/li[5]/a': 34} # Ligue 1 (France)

league_url = list(league_urls_num_matchweeks.keys())[0]
num_matchweeks = list(league_urls_num_matchweeks.values())[0]

# arguments setting -----------------------------------------------------------
parser = argparse.ArgumentParser()
parser.add_argument('--start_year', required=True)
parser.add_argument('--start_matchweek', required=False, default=None)
args = parser.parse_args()
# -----------------------------------------------------------------------------

league_name = driver.find_element(By.XPATH, league_url).text.replace(' ', '_')

print(league_name)
# cancle pop-up
try:
    driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/button').click()
except:
    pass


driver.find_element(By.XPATH, league_url).click()

#%% for loop: change years
is_begin = 1

for year_index in list(reversed(range(15)))[int(args.start_year)-2010:-1]: # change seasons


    # # temperary codes to make the code stop when it reaches to the current year season------------
    # if driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').text.split('/')[0] == str(datetime.today().year):
    #     break
    # # --------------------------------------------------------------------------------------------

    # print the season (ex. 2023/2024)
    print(driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').text)
    driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').click()

    # Counting the number of match weeks in a given season before the current match week.----
    num_matchweeks = 1

    if args.start_matchweek == None:
        num_matchweeks = 0

    for i in range(50):

        temp_current_week = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[5]/div/div/a[2]/span[1]').text

        time.sleep(1)
        driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()


        new_current_week = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[5]/div/div/a[2]/span[1]').text

        if temp_current_week == new_current_week:
            break


        num_matchweeks += 1


        

    # ----------------------------------------------------------------------------------------

    num_matchweeks = num_matchweeks

    # if args.start_year==str(datetime.today().year):
    #     num_matchweeks = num_matchweeks+1

    # go back to the target starting year
    driver.find_element(By.XPATH, league_url).click()
    driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').click()

    #%% for loop: change match week 

    # match week changes from latest to oldest one (e.g. 38->1)
    # please change 'starting_point' correctly when you run the code again after failing.
    if is_begin == 1 and args.start_matchweek!=None:
        starting_point = int(args.start_matchweek)

    else:
        starting_point = num_matchweeks
    
    if starting_point!=num_matchweeks:
        for j in range(num_matchweeks-starting_point):
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

    elif args.start_matchweek == None:
            time.sleep(1)
            driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

    is_begin = 0

    for i in range(num_matchweeks)[num_matchweeks-starting_point:]:

        current_week = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[5]/div/div/a[2]/span[1]').text

        if is_begin==1 and args.start_year==str(datetime.today().year):
            driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()
            print(f'matchweek {num_matchweeks-i}')


        else:
            print(f'matchweek {num_matchweeks-i}')


        path = f'/Users/jooyong/github_locals/Soccer_Player_Recommendation_Service/data/player_stats(from_whoscored)/Ligue_1_player_stats/'
        file_list = os.listdir(path)

        year_list = []
        for file in file_list:
            
            year_list.append(int(file.split('-')[0]))

        latest_year = max(year_list)


        path = f'/Users/jooyong/github_locals/Soccer_Player_Recommendation_Service/data/player_stats(from_whoscored)/Ligue_1_player_stats/{latest_year}-{latest_year+1}'
        file_list = os.listdir(path)

        matchweek_list = []
        for file in file_list:
            
            matchweek_list.append(int(file.split('.')[0].split('matchweek_')[1]))

        latest_matchweek = max(matchweek_list)

        print(driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').text.split('/')[0], str(latest_year))
        print(num_matchweeks-i, latest_matchweek)

        if driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').text.split('/')[0]==str(latest_year) and num_matchweeks-i == latest_matchweek:
            print('done!')
            sys.exit()


        time.sleep(5)

        matches_list = driver.find_elements(By.XPATH, f'//*[@id="tournament-fixture"]/div/div')
        #%% for loop: change match
        for match_index in range(len(matches_list)):
            
            time.sleep(10)
            one_match = {}

            if driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]').get_attribute('class')\
                != 'col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 divtable-row':
                
                time.sleep(3)

                try:
                    driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]/div[10]/a').click()
                except:
                    

                    if driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]/div[8]/a').text != "vs":
                        driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]/div[8]/a').click()
                
                    else:
                        
                        driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]/div[8]/a').click()
                        match_date = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[2]/span[3]/div[3]/dl/dd[2]').text
                        home_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[1]/a').text
                        away_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[5]/a').text

                        one_match['date'] = match_date
                        one_match['home_name'] = home_name
                        one_match['away_name'] = away_name
                        one_match['home_lineup'] = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[2]/span[3]/div[1]/dl/dd/span').text
                        one_match['away_lineup'] = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[2]/span[3]/div[1]/dl/dd/span').text
                        
                        print(match_date, home_name, 'vs', away_name)


                        with open(f'{league_name}_{2024-year_index}-{2025-year_index}_matchweek_{num_matchweeks-i}.json', 'a') as f:
                            json.dump(one_match, f)
                            f.write("\n")

                        # go back to the page includes match list
                        driver.execute_script("window.history.go(-1)")

                        # change matchweek if it is the last match in the week      

                        if match_index == len(matches_list)-1:

                            # if args.start_year==str(datetime.today().year):

                            #     driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                            for j in range(i+1):
                                time.sleep(1)
                                driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                            next_week = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[5]/div/div/a[2]/span[1]').text


                        else:
                            
                            # if args.start_year==str(datetime.today().year):

                            #     driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                            for j in range(i):
                                time.sleep(1)
                                driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()
                        continue

                    try:
                        driver.find_element(By.XPATH, '//*[@id="sub-sub-navigation"]/ul/li[3]/a').click()
                        driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/div[3]/div/div[2]/div[2]/h3/a').click()
                    except:
                        
                        
                        driver.find_element(By.XPATH, r'//*[@id="sub-navigation"]/ul/li[4]/a').click()      

                        driver.find_element(By.XPATH, r'//*[@id="sub-sub-navigation"]/ul/li[2]/a').click()

                        print(driver.find_element(By.XPATH, r'//*[@id="player-table-statistics-body"]/tr/td').text, 'for following match.')
                        if driver.find_element(By.XPATH, r'//*[@id="player-table-statistics-body"]/tr/td').text == 'There are no results to display':

                            match_date = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[2]/span[3]/div[3]/dl/dd[2]').text
                            home_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[1]/a').text
                            away_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[5]/a').text

                            one_match['date'] = match_date
                            one_match['home_name'] = home_name
                            one_match['away_name'] = away_name
                            one_match['home_lineup'] = None
                            one_match['away_lineup'] = None
                            
                            print(match_date, home_name, 'vs', away_name)

                            with open(f'{league_name}_{2024-year_index}-{2025-year_index}_matchweek_{num_matchweeks-i}.json', 'a') as f:
                                json.dump(one_match, f)
                                f.write("\n")

                        
                            # go back to the page includes match list
                            driver.execute_script("window.history.go(-4)")

                            # change matchweek if it is the last match in the week      

                            if match_index == len(matches_list)-1:

                                # if args.start_year==str(datetime.today().year):

                                #     driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                                for j in range(i+1):
                                    time.sleep(1)
                                    driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                                next_week = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[5]/div/div/a[2]/span[1]').text


                            else:
                                
                                # if args.start_year==str(datetime.today().year):

                                #     driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                                for j in range(i):
                                    time.sleep(1)
                                    driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()
                            continue

                driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/div[3]/div/div[2]/div[2]/h3/a').click()

                match_date = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[2]/span[3]/div[3]/dl/dd[2]').text
                home_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[1]/a').text
                away_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[5]/a').text

                print(match_date, home_name, 'vs', away_name)

                #%% for loop: to get player stat summary ----------------------------------
                stats_columns = ['Name', 'Position', 'Shots', 'ShotsOT', 'KeyPasses',
                                'PA%', 'AerialsWon', 'Touches', 'Rating']

                time.sleep(5)

                home_players_summary_stat_table = driver.find_element(By.ID, "live-player-home-summary").find_elements(By.TAG_NAME, 'tr')
                away_player_summary_stat_table = driver.find_element(By.ID, "live-player-away-summary").find_elements(By.TAG_NAME, 'tr')

                home_players_summary_stats = list(map(lambda x: x.text,  home_players_summary_stat_table))[1:]
                away_players_summary_stats = list(map(lambda x: x.text,  away_player_summary_stat_table))[1:]

                home_all_players_summary_stats = []
                for one_player_stats in home_players_summary_stats:
                    
            
                    one_player_stat_list = []

                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==9:

                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        home_all_players_summary_stats.append(home_single_final)


                    else:   
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])


                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        home_all_players_summary_stats.append(home_single_final)


                away_all_players_summary_stats = []
                for one_player_stats in away_players_summary_stats:

                    
                    one_player_stat_list = []

                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==9:
                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        away_all_players_summary_stats.append(away_single_final)

                    
                    else:
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])
                        
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        away_all_players_summary_stats.append(away_single_final)
                #-----------------------------------------------------------------
                #%% for loop: to get player offense stats ----------------------------------
                driver.find_element(By.XPATH, '//*[@id="live-player-home-options"]/li[2]/a').click()
                driver.find_element(By.XPATH, '//*[@id="live-player-away-options"]/li[2]/a').click()

                stats_columns = ['Name', 'Position', 'Shots', 'ShotsOT', 'KeyPasses', 'Dribbles', 'Fouled',
                                'offsides', 'Disp', 'UnsTouches', 'Rating']

                time.sleep(5)

                home_players_offensive_stat_table = driver.find_element(By.ID, "live-player-home-offensive").find_elements(By.TAG_NAME, 'tr')
                away_player_offensive_stat_table = driver.find_element(By.ID, "live-player-away-offensive").find_elements(By.TAG_NAME, 'tr')

                home_players_offensive_stats = list(map(lambda x: x.text,  home_players_offensive_stat_table))[1:]
                away_players_offensive_stats = list(map(lambda x: x.text,  away_player_offensive_stat_table))[1:]

                home_all_players_offense_stats = []
                for one_player_stats in home_players_offensive_stats:
                    
            
                    one_player_stat_list = []
                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==11:

                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        home_all_players_offense_stats.append(home_single_final)


                    else:   
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])


                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)
                        
                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        home_all_players_offense_stats.append(home_single_final)


                away_all_players_offense_stats = []
                for one_player_stats in away_players_offensive_stats:

                    
                    one_player_stat_list = []

                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==11:
                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        away_all_players_offense_stats.append(away_single_final)

                    
                    else:
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])
                        
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        away_all_players_offense_stats.append(away_single_final)
                #-----------------------------------------------------------------
                
                #%% for loop: to get player defense stats ----------------------------------
                driver.find_element(By.XPATH, '//*[@id="live-player-home-options"]/li[3]/a').click()
                driver.find_element(By.XPATH, '//*[@id="live-player-away-options"]/li[3]/a').click()

                stats_columns = ['Name', 'Position', 'TotalTackles', 'Interceptions', 'Clearances', 'BlockedShots', 'Fouls', 'Rating']

                time.sleep(5)

                home_players_defensive_stat_table = driver.find_element(By.ID, "live-player-home-defensive").find_elements(By.TAG_NAME, 'tr')
                away_player_defensive_stat_table = driver.find_element(By.ID, "live-player-away-defensive").find_elements(By.TAG_NAME, 'tr')

                home_players_defensive_stats = list(map(lambda x: x.text,  home_players_defensive_stat_table))[1:]
                away_players_defensive_stats = list(map(lambda x: x.text,  away_player_defensive_stat_table))[1:]

                home_all_players_defense_stats = []
                for one_player_stats in home_players_defensive_stats:
                    
            
                    one_player_stat_list = []
                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==8:

                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        home_all_players_defense_stats.append(home_single_final)


                    else:   
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])


                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)
                        
                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        home_all_players_defense_stats.append(home_single_final)


                away_all_players_defense_stats = []
                for one_player_stats in away_players_defensive_stats:

                    
                    one_player_stat_list = []

                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==8:
                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        away_all_players_defense_stats.append(away_single_final)

                    
                    else:
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])
                        
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        away_all_players_defense_stats.append(away_single_final)
                #-----------------------------------------------------------------

                #%% for loop: to get player passing stats ----------------------------------
                driver.find_element(By.XPATH, '//*[@id="live-player-home-options"]/li[4]/a').click()
                driver.find_element(By.XPATH, '//*[@id="live-player-away-options"]/li[4]/a').click()

                stats_columns = ['Name', 'Position', 'KeyPasses', 'Passes', 'PA%', 'Crosses', 'AccCrosses', 'LB', 'AccLB',
                                'ThB', 'AccThB', 'Rating']

                time.sleep(5)

                home_players_passing_stat_table = driver.find_element(By.ID, "live-player-home-passing").find_elements(By.TAG_NAME, 'tr')
                away_player_passing_stat_table = driver.find_element(By.ID, "live-player-away-passing").find_elements(By.TAG_NAME, 'tr')

                home_players_passing_stats = list(map(lambda x: x.text,  home_players_passing_stat_table))[1:]
                away_players_passing_stats = list(map(lambda x: x.text,  away_player_passing_stat_table))[1:]

                home_all_players_passing_stats = []
                for one_player_stats in home_players_passing_stats:
                    
            
                    one_player_stat_list = []
                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==12:

                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        home_all_players_passing_stats.append(home_single_final)


                    else:   
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])


                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)
                        
                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        home_all_players_passing_stats.append(home_single_final)


                away_all_players_passing_stats = []
                for one_player_stats in away_players_passing_stats:

                    
                    one_player_stat_list = []

                    name_stats = one_player_stats.replace('\n', '').split(',')

                    name = re.sub(r'[0-9]+', '', name_stats[0])
                    
                    position_stats = name_stats[1].split(' ')

                    if len(position_stats)==12:
                        position_stats[2] = position_stats[2].split(')')[1]

                        position = position_stats[1]
                        first_stat = position_stats[2]
                    
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[3:]))
                        away_all_players_passing_stats.append(away_single_final)

                    
                    else:
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])
                        
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        away_all_players_passing_stats.append(away_single_final)
                #-----------------------------------------------------------------



                #%% combine stats

                def merge_dicts(d_1, d_2):
                    
                    result = []

                    for one_d_1, one_d_2 in zip(d_1, d_2):

                        for key, value in one_d_2.items():

                            if key not in one_d_1.keys():

                                one_d_1[key]=value

                        result.append(one_d_1)

                    return result
                
                merge_1 = merge_dicts(home_all_players_summary_stats, home_all_players_offense_stats)
                merge_2 = merge_dicts(merge_1, home_all_players_defense_stats)
                home_merge_3 = merge_dicts(merge_2, home_all_players_passing_stats)


                merge_1 = merge_dicts(away_all_players_summary_stats, away_all_players_offense_stats)
                merge_2 = merge_dicts(merge_1, away_all_players_defense_stats)
                away_merge_3 = merge_dicts(merge_2, away_all_players_passing_stats)    

                #%% finalize one match sample
                one_match['date'] = match_date
                one_match['home_name'] = home_name
                one_match['away_name'] = away_name
                one_match['home_lineup'] = home_merge_3
                one_match['away_lineup'] = away_merge_3

                #%% save one match sample

                if args.start_year==str(datetime.today().year):

                    with open(f'{league_name}_{2024-year_index}-{2025-year_index}_matchweek_{num_matchweeks-i}.json', 'a') as f:
                        json.dump(one_match, f)
                        f.write("\n")

                else:
                    with open(f'{league_name}_{2024-year_index}-{2025-year_index}_matchweek_{num_matchweeks-i}.json', 'a') as f:
                        json.dump(one_match, f)
                        f.write("\n")

            
                #%% go back to the page includes match list
                driver.execute_script("window.history.go(-2)")

                # change matchweek if it is the last match in the week      

                if match_index == len(matches_list)-1:
                    

                    # if args.start_year==str(datetime.today().year):
                    #     driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()
                    #     print('11')
                    if args.start_matchweek==None:
                        driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()


                    for j in range(i+1):
                        time.sleep(1)
                        driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()
                    next_week = driver.find_element(By.XPATH, '/html/body/div[4]/div[3]/div[1]/div[5]/div/div/a[2]/span[1]').text


                else:
                    
                    # if args.start_year==str(datetime.today().year):
                    #     driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()
                    if args.start_matchweek==None:
                        driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                    for j in range(i):
                        time.sleep(1)  
                        driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()
            

        if current_week == next_week and args.start_year==str(datetime.today().year):
            print('done!')
            break
