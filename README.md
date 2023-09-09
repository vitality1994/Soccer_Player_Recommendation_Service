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
- Similar player recommendations
- Dashboards of a target player & similar players
    - Players’ details
    - Players’ historical stats
    - Players’ historical market values
    - Players’ play heat maps
    - Players’ general reputation
    - Expertises’ evaluations
- Player analysis
    - What analysis do other websites (TransferMarket, Squawka, Whoscored, Premier League Official, etc.) not offer?
        - Time series analysis of players’ statistics
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
5. Eredivisi (Netherlands)
6. Ligue 1 (France)
7. Liga Portugal (Portugal)
8. Jupiler Pro League (Belgium)
9. Super Lig (Türkiye)

<br>

#### Dataset descriptions

- Historical match data
    - Source: Transfer Market
    - Collecting method: Website data scraping
    - Data details:
        - Day of week
        - Day of the week
        - Match date
        - Match start / end time
        - Number of Attendance
        - Referee
        - Stadium
        - Score
        - Home / Away team name
        - Rank (at that time)
        - Home/Away managers
        - Home/Away starting lineup
        - Home/Away Substitutes
        - Home/Away event name / time
            - Goal (scorer, assister, goal type / assist type)
            - Substitution in / out / reason
            - Card receiver / type / reason

<br>

- Players' data (1)
    - Source: Transfer Market / Sofascore
    - Collecting Method: website data scraping
    - Data details:
        - From Transfer Market:
            - Date of birth
            - Nationality
            - Age
            - Height
            -  Position (Main / Sub)
            - Main foot
            - Current Team
            - Debut date
            - Start / End date of current contract
            - Market Value
            - Team with the highest probability of transfer / Probability
            - Injury History
        - From Sofascore: 
            - Attribute overview
            - Strength
            - Weaknesses
            - Seasonal heatmap
            - Seasonal stats (not overlapped with stats from Whoscored.com)

<br>

- Players' data (2)
    - Source: Whoscored
    - Collecting Method: website data scraping
    - Data details:
        - Match date
        - Home/Away team name
        - Home/Away lineups
        - Player stats (per game, not overlapped with stats from Sofascore)


<br><br>

### <center> Plans </center>

[plan for building Database](./plans/Plan_for_building_DB.md)