# Soccer_Player_Recommendation_Service

## Project Summaries

### <center> Business Problem</center> <br>
- Nowadays, soccer players' market value contains a serious market bubble for many different reasons: inflow of oil money from the Mideast, high demand for specific players, and some special rules each league has differently, such as home-grown Quota.
- There is a specific period that teams can sign new players: the Summer and winter transfer market. Therefore, if the target player has already signed with another team, starting negotiations with other players on the list of similar players to the previous target player is crucial.
- There are many leagues in the world, and each league contains many teams, and each team contains many players. 
Spending time to make the list of target players is also a cost as a business aspect.
- For the detailed analysis of the players in the list, domain experts (player scouters) need a dashboard that presents details of players.

</br>

### <center> Solution Strategy </center> <br>
- A recommendation system of similar players to the target players is to be ready if the negotiation breaks down.
- The dashboard can support domain experts (player scouters) to help them build a better transfer market strategy.

</br>

### <center> Service Details <br>
- similar player recommendations
- dashboards of a target player & similar players
    - players’ details
    - players’ historical stats
    - players’ historical market values
    - players’ play heat maps
    - players’ general reputation
    - expertises’ evaluations
- player analysis
    - What analysis do other websites (TransferMarket, Squawka, Whoscored, Premier League Official, etc.) not offer?
        - time series analysis of players’ statistics
            - Why do we care about historical stats more than the most current stats of players?
                - Players sometimes perform worse after transferring to a different team (or a different league). Analyze historical stats of players to understand what could be the factors.
            - Historical stats are a good reference to check the general trend of players’ performance (per match, against rival teams, seasonal, etc.) 

<br><br>

### <center> Data details </center> <br>

#### Target leagues list (ordered by UEFA coefficients)
1. Premier League (England)
2. Laliga (Spain)
3. Seria-A (Italy)
4. Bundesliga (Germany)
5. ~~Eredivisi (Netherlands)~~
6. Ligue 1 (France)
7. ~~Liga Portugal (Portugal)~~
8. ~~Jupiler Pro League (Belgium)~~
9. ~~Super Lig (Türkiye)~~

<br>

#### Dataset descriptions

- historical match data
    - source: Transfer Market
    - collecting method: website data scraping
    - data details:
        - match general info
            - day of week
            - match date
            - match start / end time
            - stadium
            - number of Attendance
            - referee
            - score
        - team details
            - home team
                - team name
                - rank (at the time the match was held)
                - starting lineup
                - substitutes
                - manager
            - away team
                - team name
                - rank (at the time the match was held)
                - starting lineup
                - substitutes
                - manager
        - event details
            - home team
                - goal
                    - scorer
                    - goal type
                    - assister
                    - assist type
                    - time
                - card
                    - name
                    - card type
                    - reason
                    - time
                - sub
                    - subs in (name)
                    - subs out (name)
                    - subs out reason
                    - time
            - away team
                - goal
                    - scorer
                    - goal type
                    - assister
                    - assist type
                    - time
                - card
                    - name
                    - card type
                    - reason
                    - time
                - sub
                    - subs in (name)
                    - subs out (name)
                    - subs out reason
                    - time

<br>

- players' data (1)
    - source: Transfer Market / Sofascore
    - collecting method: website data scraping
    - data details:
        - from Transfer Market:
            - date of birth
            - nationality
            - age
            - height
            - position (Main / Sub)
            - main foot
            - current Team
            - debut date
            - start / end date of current contract
            - market value
            - team with the highest probability of transfer / probability
            - injury history
        - from Sofascore: 
            - attribute overview
            - strength
            - weaknesses
            - seasonal heatmap
            - seasonal stats (not overlapped with stats from Whoscored.com)

<br>

- players' data - match stats
    - source: Whoscored
    - collecting method: website data scraping
    - data details:
        - match date
        - home team name 
        - away team name
        - home lineup
            - player name
            - position
            - match stat 1
            - match stat 2 
            - ... <br>
            *for all starting lineups + subs
        - away lineup
            - player name
            - position
            - match stat 1
            - match stat 2 
            - ... <br>
            *for all starting lineups + subs



<br><br>

### <center> Plans </center>

[plan for building Database](./plans/Plan_for_building_DB.md)

collecting data

build database

![image](Soccer%20Player%20Recommender.png)
