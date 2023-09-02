#%% import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re


#%% read html of specific league, specific season, specific matchweek main page
url = "https://www.transfermarkt.com/premier-league/spieltagtabelle/wettbewerb/GB1?saison_id=2010&spieltag=1"
header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15'}

page = requests.get(url, headers=header)

soup = BeautifulSoup(page.text, features='lxml')

#%% create a list of matches during in a matchweek
parsed_matches = list(soup.find('div', class_ = 'large-8 columns').find_all('a', title = 'Match report'))
list_matches_url = list(map(lambda x: "https://www.transfermarkt.com"+x['href'], parsed_matches))
# %%
match_detail_list = []

match_detail_dict = {}



#%%
for match_url in list_matches_url:

    one_match_url = match_url
    
    one_match_page = requests.get(one_match_url, headers=header)
    one_match_soup = BeautifulSoup(one_match_page.text, features='lxml')

    # extract match score
    score_re = re.compile('[0-9]{1,2}:[0-9]{1,2}')
    score_par = one_match_soup.find('div', class_ = 'sb-endstand').text
    match_score = score_re.findall(score_par)[0]

    # extract match date, start time

    match_day_date = list(one_match_soup.find('p', class_ = 'sb-datum hide-for-small').find_all('a'))[1]\
                    .text.replace(' ', '').replace('\n', '').split(',')

    match_day_name = match_day_date[0]
    match_date = match_day_date[1]

    timestamp_pat = re.compile('[0-9]{1,2}:[0-9]{1,2} [A-Za-z]{2}')
    match_starttime_parsed = one_match_soup.find('div', class_ = 'box sb-spielbericht-head')

    match_starttime = timestamp_pat.findall(match_starttime_parsed.text)[0]


    # extract home teamname & ranking at that time 
    match_home_name_rank = one_match_soup.find('div', class_='sb-team sb-heim').text.split(' Position:')

    match_home_name = match_home_name_rank[0].replace('\n ', '')

    rank_re = re.compile('\d{1,2}')
    match_home_rank = rank_re.findall(match_home_name_rank[1])[0]



    # extract away teamname & ranking at that time 
    match_away_name_rank = one_match_soup.find('div', class_='sb-team sb-gast').text.split(' Position:')

    match_away_name = match_away_name_rank[0].replace('\n ', '')

    rank_re = re.compile('\d{1,2}')
    match_away_rank = rank_re.findall(match_away_name_rank[1])[0]



    # extract stadium, referee, attendance

    match_stadium_attendance_referee = one_match_soup.find('p', class_ = "sb-zusatzinfos")

    match_stadium_referee_parsed = match_stadium_attendance_referee.findAll('a')
    match_stadium_referee_list = list(map(lambda x: x.text, match_stadium_referee_parsed))

    match_stadium = match_stadium_referee_list[0]
    match_referee = match_stadium_referee_list[1]
    match_attendance = match_stadium_attendance_referee.find('strong').text.split(': ')[1]

    


    # record match data in a dict

    match_detail_dict['match_day'] = match_day_name
    match_detail_dict['match_date'] = match_date
    match_detail_dict['match_starttime'] = match_starttime
    match_detail_dict['match_stadium'] = match_stadium
    match_detail_dict['match_referee'] = match_referee
    match_detail_dict['match_score'] = match_score
    match_detail_dict['match_home_name'] = match_home_name
    match_detail_dict['match_home_rank'] = match_home_rank
    match_detail_dict['match_away_name'] = match_away_name
    match_detail_dict['match_away_rank'] = match_away_rank


    match_detail_list.append(match_detail_dict)
    match_detail_dict = {}

#%%
for i in match_detail_list:

    print(i) 

# 9.1.2023 record: this code scrapes such match details
    # match day
    # match date
    # match starttime
    # match stadium
    # match referee
    # match score
    # match hometeam name
    # match hometeam rank (at that time)
    # match awayteam name
    # match awayteam rank (at that time) 