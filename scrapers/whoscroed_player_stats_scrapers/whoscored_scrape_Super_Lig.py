#%% import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import time
import json
from fake_headers import Headers

import warnings
warnings.filterwarnings("ignore")

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

#%% Run web scraping 

website = 'https:/1xbet.whoscored.com'
path = '/Users/jooyong/Downloads/chromedriver-mac-arm64/chromedriver'

driver = webdriver.Chrome(path, chrome_options=options)
driver.implicitly_wait(20)

driver.get(website)

#list of league urls
league_urls_num_matchweeks = {'//*[@id="popular-tournaments-list"]/li[11]/a': 38} # Super lig (Turkey)


# cancle pop-up
driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/button').click()


#%% for loop: change league
for league_url, num_matchweeks in league_urls_num_matchweeks.items():

    league_name = driver.find_element(By.XPATH, league_url).text.replace(' ', '_')

    print(league_name)
    # pick specific league 
    driver.find_element(By.XPATH, league_url).click()

    #%% for loop: change years
    for year_index in list(reversed(range(15)))[:-1]: # change seasons

        one_season_total = []

        print(driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').text)
        driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').click()

        #%% for loop: change match week 

        # match week changes from latest to oldest one (e.g. 38->1)
        # please change 'starting_point' correctly when you run the code again after failing.
        starting_point = num_matchweeks

        if starting_point!=38:
            for j in range(num_matchweeks-starting_point):
                time.sleep(1)
                driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

        for i in range(num_matchweeks)[num_matchweeks-starting_point:]:
            
            print(f'matchweek {num_matchweeks-i}')
            time.sleep(5)

            matches_list = driver.find_elements(By.XPATH, f'//*[@id="tournament-fixture"]/div/div')
            #%% for loop: change match
            for match_index in range(len(matches_list)):
                
                time.sleep(10)
                one_match = {}

                if driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]').get_attribute('class')\
                    != 'col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 divtable-row':
                   
                    time.sleep(3)

                    driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]/div[10]/a').click()
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

                    with open(f'{league_name}_{2024-year_index}-{2025-year_index}_matchweek_{num_matchweeks-i}.json', 'a') as f:
                        json.dump(one_match, f)
                        f.write("\n")

                
                    #%% go back to the page includes match list
                    driver.execute_script("window.history.go(-2)")

                    # change matchweek if it is the last match in the week      

                    if match_index == len(matches_list)-1:
                        for j in range(i+1):
                            time.sleep(1)
                            driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()

                    else:
                        for j in range(i):
                            time.sleep(1)
                            driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()


#%%
