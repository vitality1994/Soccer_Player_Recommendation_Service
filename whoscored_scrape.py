#%%
from selenium import webdriver
from selenium.webdriver.common.by import By
import requests
import re
import time

# %%
website = 'https:/1xbet.whoscored.com'

path = '/Users/jooyong/Downloads/chromedriver-mac-arm64/chromedriver'


driver = webdriver.Chrome(path)

driver.get(website)

time.sleep(1)
driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/button').click()
driver.find_element(By.XPATH, '//*[@id="popular-tournaments-list"]/li[1]/a').click()
driver.find_element(By.XPATH, '//*[@id="seasons"]/option[14]').click()

matches_list = driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div')


test_2 = matches_list.find_elements(By.CLASS_NAME, 'divtable-row.col12-lg-12.col12-m-12.col12-s-12.col12-xs-12.')
test_1 = matches_list.find_elements(By.CLASS_NAME, 'divtable-row col12-lg-12 col12-m-12 col12-s-12 col12-xs-12 alt'.replace(' ', '.'))

print(len(test_1))
print(len(test_2))


for i in matches_list:


    print(i.get_attribute('class'))
    if i.get_attribute('class') == 'match-link match-report rc':

        time.sleep(3)

        i.click()

        time.sleep(3)

        driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/div[3]/div/div[2]/div[2]/h3/a').click()



        stats_columns = ['Name', 'Position', 'Shots', 'ShotsOT', 'KeyPasses',
                        'PA%', 'AerialsWon', 'Touches', 'Rating']

        single_player_stats = {}

        time.sleep(1)

        player_stat_table = driver.find_elements(By.ID, "player-table-statistics-body")
        player_stat_table_fixed = list(map(lambda x: x.find_elements(By.TAG_NAME, 'tr'), player_stat_table))
        home_players_stats = list(map(lambda x: x.text,  player_stat_table_fixed[0]))
        away_players_stats = list(map(lambda x: x.text,  player_stat_table_fixed[1]))


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

                print(dict(zip(stats_columns, one_player_stat_list+position_stats[3:])))  


            else:   
                position = re.sub(r'[0-9]+', '', position_stats[1])
                
                first_stat = re.sub(r'[^0-9]+', '', position_stats[1])


                one_player_stat_list.append(name)
                one_player_stat_list.append(position)
                one_player_stat_list.append(first_stat)

                print(dict(zip(stats_columns, one_player_stat_list+position_stats[2:])))    




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

                print(dict(zip(stats_columns, one_player_stat_list+position_stats[3:])))  


            
            else:
                position = re.sub(r'[0-9]+', '', position_stats[1])
                
                first_stat = re.sub(r'[^0-9]+', '', position_stats[1])
                
                one_player_stat_list.append(name)
                one_player_stat_list.append(position)
                one_player_stat_list.append(first_stat)

                print(dict(zip(stats_columns, one_player_stat_list+position_stats[2:])))  

        driver.back()
        driver.back()

#%%
# close the chrome
driver.quit()


