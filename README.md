# Soccer_Player_Recommendation_Service

## Project Summaries

### <center> Why a data-driven player recommendation service is necessary?</center>
- Nowadays, soccer players' market value contains a serious market bubble for many different reasons: inflow of oil money from the Mideast, high demand for specific players, and some special rules each league has differently, such as home-grown Quota.
- There is a specific period that teams can sign new players: the Summer and Winter transfer market. Therefore, if the target player has already signed with another team, starting negotiations with other players on the list of similar players to the previous target player is crucial.
- There are many leagues in the world, and each league contains many teams, and each team contains many players. 
Spending time to make the list of target players is also a cost as a business aspect.
- For the detailed analysis of the players in the list, domain experts (player scouters) need a dashboard that presents details of players.

</br>

### <center> What are the benefits of this service? </center>
- A recommendation system of similar players to the target players is to be ready if the negotiation breaks down.
- The dashboard can support domain experts (player scouters) to help them build a better transfer market strategy.

</br>

### <center> What services are provided by this project? <br>
- similar player recommendations
- dashboards of a target player & similar players
    - players’ details
    - players’ historical stats
    - players’ historical market values
    - players’ play heat maps
    - players’ general reputation
    - expertises’ evaluations
- player analysis
    - analysis other websites (TransferMarket, Squawka, Whoscored, Premier League Official, etc.) does not offer
        - time series analysis of players’ statistics <br>
            - Historical stats are a good reference to check the general trend of players’ performance.

<br><br>

### <center> What data is used? </center> <br>

leagues currently included in the dataset:
- Premier League (England)
- Laliga (Spain)
- Seria-A (Italy)
- Bundesliga (Germany)
- Ligue 1 (France)

leagues could be added in the future:
- Eredivisi (Netherlands)
- Liga Portugal (Portugal)
- Jupiler Pro League (Belgium)
- Super Lig (Türkiye)

<br>

#### Dataset Descriptions

- historical match <span style = "background-color: #DEFFE4">(collected)</span>
    - source: Transfer Market
    - collecting method: website data scraping
    - data details:
        - match general info
            - day of week
            - match date
            - match starttime
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

- players' data - match stats <span style = "background-color: #DEFFE4">(collected)</span>
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

<br>

- players' data - players' info <span style = "background-color: #FFE6E6">(not collected yet)</span>
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
