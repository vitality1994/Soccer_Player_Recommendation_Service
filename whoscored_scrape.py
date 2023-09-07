#%% import packages
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import time


#%% Run web scraping 

website = 'https:/1xbet.whoscored.com'
path = '/Users/jooyong/Downloads/chromedriver-mac-arm64/chromedriver'

driver = webdriver.Chrome(path)
driver.implicitly_wait(20)

driver.get(website)

# cancle pop-up
driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/button').click()
# pick specific league (current url: Premier League)
driver.find_element(By.XPATH, '//*[@id="popular-tournaments-list"]/li[1]/a').click()



for year_index in list(reversed(range(15))): # change seasons

    driver.find_element(By.XPATH, f'//*[@id="seasons"]/option[{year_index}]').click()

    # change match week (current: 38 for Premier league)
    for i in range(38):
        
        time.sleep(5)
        matches_list = driver.find_elements(By.XPATH, f'//*[@id="tournament-fixture"]/div/div')

        for match_index in range(len(matches_list))[-1:]:

            one_match = {}

            if driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]').get_attribute('class')\
                != 'col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 divtable-row':

                driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{match_index+1}]/div[10]/a').click()
                driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/div[3]/div/div[2]/div[2]/h3/a').click()


                # to get player stat summary ----------------------------------

                stats_columns = ['Name', 'Position', 'Shots', 'ShotsOT', 'KeyPasses',
                                'PA%', 'AerialsWon', 'Touches', 'Rating']

                single_player_stats = {}

                time.sleep(5)
                match_date = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[2]/span[3]/div[3]/dl/dd[2]').text

                home_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[1]/a').text
                away_name = driver.find_element(By.XPATH, '//*[@id="match-header"]/div/div[1]/span[5]/a').text

                
                driver.find_element(By.XPATH, '//*[@id="live-player-home-options"]/li[2]/a').click

                player_stat_table = driver.find_elements(By.ID, "player-table-statistics-body")
                player_stat_table_fixed = list(map(lambda x: x.find_elements(By.TAG_NAME, 'tr'), player_stat_table))

                home_players_stats = list(map(lambda x: x.text,  player_stat_table_fixed[0]))
                away_players_stats = list(map(lambda x: x.text,  player_stat_table_fixed[1]))

                home_all_players_stats = []
                for one_player_stats in home_players_stats:
                    
            
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
                        home_all_players_stats.append(home_single_final)


                    else:   
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])


                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        home_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        home_all_players_stats.append(home_single_final)


                away_all_players_stats = []
                for one_player_stats in away_players_stats:

                    
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
                        away_all_players_stats.append(away_single_final)

                    
                    else:
                        position = re.sub(r'[0-9]+', '', position_stats[1])
                        
                        first_stat = re.sub(r'[^0-9]+', '', position_stats[1])
                        
                        one_player_stat_list.append(name)
                        one_player_stat_list.append(position)
                        one_player_stat_list.append(first_stat)

                        away_single_final = dict(zip(stats_columns, one_player_stat_list+position_stats[2:]))
                        away_all_players_stats.append(away_single_final)

                #-----------------------------------------------------------------

                # need code block to get player offense stats
                
                # need code block to get player defenses stats

                # need code block to get playter pass stats



                # one sample shoud look like...
                # {date: , home_team: , away_team: } -> print
                # 위 처럼해야 나중에 match_detail하고 맞출 수 있음.

                one_match['date'] = match_date
                one_match['home_name'] = home_name
                one_match['away_name'] = away_name
                one_match['home_lineup'] = home_all_players_stats
                one_match['away_lineup'] = away_all_players_stats

                print(one_match)

                driver.execute_script("window.history.go(-2)")

                if match_index+1 == len(matches_list):
                    
                    for j in range(i+1):
                        time.sleep(1)
                        driver.find_element(By.XPATH, '//*[@id="date-controller"]/a[1]').click()


# %%

