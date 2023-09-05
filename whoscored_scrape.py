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


driver.find_element(By.XPATH, '/html/body/div[7]/div/div[1]/button').click()
driver.find_element(By.XPATH, '//*[@id="popular-tournaments-list"]/li[1]/a').click()
driver.find_element(By.XPATH, '//*[@id="seasons"]/option[14]').click()

for i in range(10):

    if i!=0 and i!=1 and i!=3:

        driver.find_element(By.XPATH, f'//*[@id="tournament-fixture"]/div/div[{i}]/div[10]/a').click()
        driver.find_element(By.XPATH, '//*[@id="layout-wrapper"]/div[3]/div/div[2]/div[2]/h3/a').click()



        stats_columns = ['Name', 'Position', 'Shots', 'ShotsOT', 'KeyPasses',
                        'PA%', 'AerialsWon', 'Touches', 'Rating']

        single_player_stats = {}

        time.sleep(1)

        players_stats = list(map(lambda x: x.text, driver.find_elements(By.TAG_NAME, 'tr')))[1:]



        for one_player_stats in players_stats[:18]:

            one_player_stat_list = []

            name_stats = one_player_stats.replace('\n', '').split(',')

            name = re.sub(r'[0-9]+', '', name_stats[0])
            
            position_stats = name_stats[1].split(' ')

            position = re.sub(r'[0-9]+', '', position_stats[1])
            
            first_stat = re.sub(r'[^0-9]+', '', position_stats[1])


            one_player_stat_list.append(name)
            one_player_stat_list.append(position)
            one_player_stat_list.append(first_stat)

            print(dict(zip(stats_columns, one_player_stat_list+position_stats[2:])))    


        for one_player_stats in players_stats[-18:]:

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



#%%
players_stats[-18:][6].replace('\n', '').split(',')[1].split(' ')



#%%
# close the chrome
driver.quit()

#%%
re.sub(r'[0-9]+', '', '123cdd432')


# %%
