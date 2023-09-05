# import packages
import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
from timeit import default_timer as timer
import cchardet
import json
import ndjson


def scrape_match_details_from_TM(start_year, start_matchweek):
    


    requests_session = requests.Session()


    for year in list(range(start_year,2024)):

        season_name = 'season '+str(year)+'/'+str(year+1)

        print('\n\n'+season_name)


        if year==start_year:

            start_matchweek_input = start_matchweek-1
        
        else:

            start_matchweek_input = 0


        for matchweek in list(range(38))[start_matchweek_input:]:


            print('\nmatchweek: '+str(matchweek+1))

            url = f"https://www.transfermarkt.com/premier-league/spieltagtabelle/wettbewerb/GB1?saison_id={year}&spieltag={matchweek+1}"
            header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Safari/605.1.15'}

            page = requests_session.get(url, headers=header)

            soup = BeautifulSoup(page.text, features='lxml')

            # create a list of matches during in a matchweek
            parsed_matches = list(soup.find('div', class_ = 'large-8 columns').find_all('a', title = 'Match report'))
            list_matches_url = list(map(lambda x: "https://www.transfermarkt.com"+x['href'], parsed_matches))


            match_detail_dict = {}


            for one_match_url in list_matches_url:

                one_match_url = one_match_url
                one_match_page = requests_session.get(one_match_url, headers=header)
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


                if match_stadium_attendance_referee.find('span', class_='hide-for-small').find('strong')==None:

                    match_attendance = None
                
                else:
                    match_attendance = match_stadium_attendance_referee.find('strong').text.split(': ')[1]


                # extract event type & time

                home_events_par = one_match_soup.find('div', class_ = 'sb-leiste-heim')
                home_events_list = home_events_par.findAll('div', class_ = "sb-leiste-ereignis")

                home_event_times = list(map(lambda x: round(float(x['style'].split(': ')[1][:-2])*90/100), home_events_list))

                home_events_time_dict = {}
                home_goal_time_list = []
                home_card_time_list = []
                home_sub_time_list = []

                home_event_names = list(map(lambda x: x.find('span')['class'][1], home_events_list))
                home_event_time_pairs = list(zip(home_event_names, home_event_times))


                for type, time in home_event_time_pairs:
                    
                    if type == 'sb-gelb' or type == 'sb-gelbrot' or type == 'sb-rot':
                        home_card_time_list.append(time)
                    
                    elif type == 'sb-tor' or type == 'sb-eigentor':
                        
                        home_goal_time_list.append(time)
                    
                    elif type == 'sb-wechsel':
                        
                        home_sub_time_list.append(time)

                home_events_time_dict['goals'] = home_goal_time_list
                home_events_time_dict['cards'] = home_card_time_list
                home_events_time_dict['subs'] = home_sub_time_list



                away_events_par = one_match_soup.find('div', class_ = 'sb-leiste-gast')
                away_events_list = away_events_par.findAll('div', class_ = "sb-leiste-ereignis")

                away_event_times = list(map(lambda x: round(float(x['style'].split(': ')[1][:-2])*90/100), away_events_list))

                away_events_time_dict = {}
                away_goal_time_list = []
                away_card_time_list = []
                away_sub_time_list = []

                away_event_names = list(map(lambda x: x.find('span')['class'][1], away_events_list))
                away_event_time_pairs = list(zip(away_event_names, away_event_times))

                for type, time in away_event_time_pairs:
                    
                    if type == 'sb-gelb' or type == 'sb-gelbrot' or type == 'sb_rot':
                        
                        away_card_time_list.append(time)
                    
                    elif type == 'sb-tor' or type == 'sb-eigentor':
                        
                        away_goal_time_list.append(time)
                    
                    elif type == 'sb-wechsel':
                        
                        away_sub_time_list.append(time)


                away_events_time_dict['goals'] = away_goal_time_list
                away_events_time_dict['cards'] = away_card_time_list
                away_events_time_dict['subs'] = away_sub_time_list




                # extract home goals info data

                

                match_goals_info = {'home':[], 'away':[]}

                if len(home_goal_time_list)!=0:

                    home_goal_info_par = one_match_soup.find('div', class_ = 'sb-ereignisse', id='sb-tore').findAll('li', class_='sb-aktion-heim')

                    home_goal_info_par_fix = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').text, home_goal_info_par))

                    for goal_assist_info in home_goal_info_par_fix:

                        home_goals_info = {}

                        goal_info_edited = goal_assist_info.replace('\n', '').split('Assist: ')[0].split(',')
                        home_scorer = goal_info_edited[0]
                        home_goal_type = goal_info_edited[1].strip()


                        if len(goal_assist_info.replace('\n', '').split('Assist: '))!=1:
                            assist_info_edited = goal_assist_info.replace('\n', '').split('Assist: ')[1].split(',')


                            if len(assist_info_edited)!=1: # if there is no assister
                                
                                if len(assist_info_edited)==3:
                                    home_assister = assist_info_edited[0]
                                    home_assist_type = assist_info_edited[1].strip()

                                elif len(assist_info_edited)==2:
                                    home_assister = assist_info_edited[0]
                                    home_assist_type = 'foul'
                            
                            else:
                                home_assister = None
                                home_assist_type =None
                        else:

                            home_assister = None
                            home_assist_type =None

                        home_goals_info['scorer'] = home_scorer
                        home_goals_info['goal_type'] = home_goal_type
                        home_goals_info['assister'] = home_assister
                        home_goals_info['assist_type'] = home_assist_type

                        match_goals_info['home'].append(home_goals_info)


                        
                        
                # extract away goals info data

                if len(away_goal_time_list)!=0:

                    away_goal_info_par = one_match_soup.find('div', class_ = 'sb-ereignisse', id='sb-tore').findAll('li', class_='sb-aktion-gast')

                    away_goal_info_par_fix = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').text, away_goal_info_par))



                    for goal_assist_info in away_goal_info_par_fix:

                        away_goals_info = {}

                        goal_info_edited = goal_assist_info.replace('\n', '').split('Assist: ')[0].split(',')
                        away_scorer = goal_info_edited[0]
                        away_goal_type = goal_info_edited[1].strip()

                        
                        if len(goal_assist_info.replace('\n', '').split('Assist: '))!=1:

                            assist_info_edited = goal_assist_info.replace('\n', '').split('Assist: ')[1].split(',')


                            if len(assist_info_edited)!=1: # if there is no assister.
                            
                                if len(assist_info_edited)==3:

                                    away_assister = assist_info_edited[0]
                                    away_assist_type = assist_info_edited[1].strip()
                                
                                elif len(assist_info_edited)==2:

                                    away_assister = assist_info_edited[0]
                                    away_assist_type = 'faul'
                            
                            else:

                                away_assister = None
                                away_assist_type = None
                        
                        else:
                            away_assister = None
                            away_assist_type = None

                        away_goals_info['scorer'] = away_scorer
                        away_goals_info['goal_type'] = away_goal_type
                        away_goals_info['assister'] = away_assister
                        away_goals_info['assist_type'] = away_assist_type

                        match_goals_info['away'].append(away_goals_info)


                # extract home substitution data

                subs_info_dict = {'home': [], 'away': []}

                if len(home_sub_time_list)!=0:

                    home_subs_info_par = one_match_soup.find('div', class_ = 'sb-ereignisse', id='sb-wechsel').findAll('li', class_='sb-aktion-heim')


                    home_subs_in = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').find('span', class_='sb-aktion-wechsel-ein').find('a'), home_subs_info_par))


                    home_subs_out_name = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').find('span', class_='sb-aktion-wechsel-aus').find('a').text, home_subs_info_par))
                    home_subs_out_reason = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').find('span', class_='sb-aktion-wechsel-aus').find('span', class_='hide-for-small')\
                                                    .text.replace(', ', '').replace('\xa0', ''), home_subs_info_par))

                    for subs_in_name, subs_out_name, subs_out_reason in zip(home_subs_in, home_subs_out_name, home_subs_out_reason):
                        home_subs_dict = {}

                        if subs_in_name!=None:
                            home_subs_dict['subs_in'] = subs_in_name.text

                        else:
                            home_subs_dict['subs_in'] = None

                        home_subs_dict['subs_out'] = subs_out_name
                        home_subs_dict['subs_out_reason'] = subs_out_reason

                        subs_info_dict['home'].append(home_subs_dict)



                # extract away substitution data

                if len(away_sub_time_list)!=0:

                    away_subs_info_par = one_match_soup.find('div', class_ = 'sb-ereignisse', id='sb-wechsel').findAll('li', class_='sb-aktion-gast')

                    away_subs_in = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').find('span', class_='sb-aktion-wechsel-ein').find('a'), away_subs_info_par))


                    away_subs_info_par = one_match_soup.find('div', class_ = 'sb-ereignisse', id='sb-wechsel').findAll('li', class_='sb-aktion-gast')

                    away_subs_out_name = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').find('span', class_='sb-aktion-wechsel-aus').find('a').text, away_subs_info_par))
                    away_subs_out_reason = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').find('span', class_='sb-aktion-wechsel-aus').find('span', class_='hide-for-small')\
                                                    .text.replace(', ', '').replace('\xa0', ''), away_subs_info_par))


                    for subs_in_name, subs_out_name, subs_out_reason in zip(away_subs_in, away_subs_out_name, away_subs_out_reason):
                        away_subs_dict = {}

                        if subs_in_name!=None:
                            away_subs_dict['subs_in'] = subs_in_name.text

                        else:
                            away_subs_dict['subs_in'] = None

                        away_subs_dict['subs_out'] = subs_out_name
                        away_subs_dict['subs_out_reason'] = subs_out_reason

                        subs_info_dict['away'].append(away_subs_dict)



                # home card record
                card_info_dict = {'home':[], 'away':[]}

                if len(home_card_time_list)!=0:

                    home_card_info_par = one_match_soup.find('div', class_='sb-ereignisse', id='sb-karten').findAll('li', class_='sb-aktion-heim')
                    home_card_info_par_fixed = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').text.split('\n'), home_card_info_par))

                    home_card_info_list = []
                    for single_case in home_card_info_par_fixed:

                        home_card_dict = {}

                        name = single_case[0].strip()

                        type_reason = single_case[1].split(',')

                        card_type = re.sub(r'[0-9][^\uAC00-\uD7A30-9a-zA-Z\s]', '', type_reason[0]).strip()

                        if len(type_reason) == 1:
                            
                            reason = None

                        else:
                            reason = type_reason[1].strip()

                        home_card_dict['name'] = name
                        home_card_dict['card_type'] = card_type
                        home_card_dict['reason'] = reason

                        card_info_dict['home'].append(home_card_dict)



                # away card record

                if len(away_card_time_list) != 0:
                
                    away_card_info_par = one_match_soup.find('div', class_='sb-ereignisse', id='sb-karten').findAll('li', class_='sb-aktion-gast')
                    away_card_info_par_fixed = list(map(lambda x: x.find('div', class_ = 'sb-aktion-aktion').text.split('\n'), away_card_info_par))

                    away_card_info_list = []
                    for single_case in away_card_info_par_fixed:

                        away_card_dict = {}
                        
                        name = single_case[0].strip()

                        type_reason = single_case[1].split(',')

                        card_type = re.sub(r'[0-9][^\uAC00-\uD7A30-9a-zA-Z\s]', '', type_reason[0]).strip()

                        if len(type_reason) == 1:

                            reason = None
                        
                        else:
                            reason = type_reason[1].strip()

                        away_card_dict['name'] = name
                        away_card_dict['card_type'] = card_type
                        away_card_dict['reason'] = reason

                        card_info_dict['away'].append(away_card_dict)



                home_events = home_events_time_dict
                home_goals = match_goals_info['home']
                home_subs = subs_info_dict['home']
                home_cards = card_info_dict['home']

                home_event_details_dict = {}

                home_goal_details_list = []
                for time, goal in zip(home_events['goals'], home_goals):
                    
                    goal['time']=time
                    home_goal_details_list.append(goal)

                    home_event_details_dict['goal'] = home_goal_details_list


            

                home_card_details_list = []
                for time, card in zip(home_events['cards'], home_cards):

                    card['time']=time
                    home_card_details_list.append(card)

                    home_event_details_dict['card'] = home_card_details_list


                home_sub_details_list = []
                for time, sub in zip(home_events['subs'], home_subs):

                    sub['time'] = time
                    home_sub_details_list.append(sub)

                    home_event_details_dict['sub'] = home_sub_details_list



                away_events = away_events_time_dict
                away_goals = match_goals_info['away']
                away_subs = subs_info_dict['away']
                away_cards = card_info_dict['away']



                away_event_details_dict = {}

                away_goal_details_list = []
                for time, goal in zip(away_events['goals'], away_goals):
                    
                    goal['time']=time
                    away_goal_details_list.append(goal)

                    away_event_details_dict['goal'] = away_goal_details_list


                away_card_details_list = []
                for time, card in zip(away_events['cards'], away_cards):
                    
                    card['time']=time
                    away_card_details_list.append(card)

                    away_event_details_dict['card'] = away_card_details_list


                away_sub_details_list = []
                for time, sub in zip(away_events['subs'], away_subs):

                    sub['time'] = time
                    away_sub_details_list.append(sub)

                    away_event_details_dict['sub'] = away_sub_details_list



                match_detail_dict = {'match_general_info':{}, 'team_details':{}, 'event_details':{}}

                match_detail_dict['match_general_info']['day'] = match_day_name
                match_detail_dict['match_general_info']['date'] = match_date
                match_detail_dict['match_general_info']['starttime'] = match_starttime
                match_detail_dict['match_general_info']['stadium'] = match_stadium
                match_detail_dict['match_general_info']['attendance'] = match_attendance
                match_detail_dict['match_general_info']['referee'] = match_referee
                match_detail_dict['match_general_info']['score'] = match_score



                match_detail_dict['event_details']['home'] = home_event_details_dict
                match_detail_dict['event_details']['away'] = away_event_details_dict


                match_lineup_url = one_match_soup.find('li', id='line-ups').find('a')['href']

                one_match_lineup_page = requests_session.get("https://www.transfermarkt.com"+match_lineup_url, headers=header)
                one_match_lineup_soup = BeautifulSoup(one_match_lineup_page.text, features='lxml')
                

                starting_lineups = one_match_lineup_soup.findAll('div', class_ = 'row sb-formation')[0]
                substitutes = one_match_lineup_soup.findAll('div', class_ = 'row sb-formation')[1]
                managers = one_match_lineup_soup.findAll('div', class_ = 'row sb-formation')[2]
                

                home_starting_lineups_par = starting_lineups.findAll('div', class_='large-6 columns')[0].find('table', class_='items').findAll('a', class_='wichtig')
                home_starting_lineups_list = list(map(lambda x: x.text, home_starting_lineups_par))
                
                away_starting_lineups_par = starting_lineups.findAll('div', class_='large-6 columns')[1].find('table', class_='items').findAll('a', class_='wichtig')
                away_starting_lineups_list = list(map(lambda x: x.text, away_starting_lineups_par))

                home_subplayer_par = substitutes.findAll('div', class_='large-6 columns')[0].find('table', class_='items').findAll('a', class_='wichtig')
                home_subplayer_list = list(map(lambda x: x.text, home_subplayer_par))
                
                away_subplayer_par = substitutes.findAll('div', class_='large-6 columns')[1].find('table', class_='items').findAll('a', class_='wichtig')
                away_subplayer_list = list(map(lambda x: x.text, away_subplayer_par))

                home_manager = managers.findAll('div', class_='large-6 columns')[0].find('table', class_='items').findAll('a', class_='wichtig')[0].text
                away_manager = managers.findAll('div', class_='large-6 columns')[1].find('table', class_='items').findAll('a', class_='wichtig')[0].text


                match_detail_dict['team_details']['home'] = {'name': match_home_name,
                                                            'rank': match_home_rank,
                                                            'starting_line_up': home_starting_lineups_list,
                                                            'substitutes': home_subplayer_list,
                                                            'manager': home_manager}
                match_detail_dict['team_details']['away'] = {'name': match_away_name,
                                                            'rank': match_away_rank,
                                                            'starting_line_up': away_starting_lineups_list,
                                                            'substitutes': away_subplayer_list,
                                                            'manager': away_manager}
                

                print(match_detail_dict['team_details']['home']['name'], 'vs', match_detail_dict['team_details']['away']['name'])
                
                with open('data.json', 'a') as f:
                    json.dump(match_detail_dict, f)
                    f.write("\n")


scrape_match_details_from_TM(start_year=2019, start_matchweek=28)