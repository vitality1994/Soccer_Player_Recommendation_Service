[DB type cheet sheet](../knowledges/Types_of_Databases.md)

Article: The important thing to think about before choosing which database type should be used to keep data quality.
* [Data Quality Metrics for Data Warehouses](https://www.metaplane.dev/blog/data-quality-metrics-for-data-warehouses)


</br></br>


Thoughts

Data consistency is the most crucial factor for the recommendation system and dashboards. Real-time data update is unnecessary because players' stat and details will not differ dramatically after a few more games. In terms of this, the relational database could be a choice we can think about.

However, to do a deeper analysis, I will scrape historical match data to track how players' performance changed in different circumstances(e.g., during a game with a rival team, performance fluctuation, etc.). <mark>Each match data has different events (e.g., goal, red card, etc.) at different times, and those make it hard to keep the same columns of the table containing match data if I use a relational database to keep data. Therefore, using a NoSQL database such as MongoDB is one of the choices if I can keep data consistency as much as possible.</mark> 

As one of the types of NoSQL database, Graph database Neo4j could be suitable for this project, defining the team, match, and player as graph nodes. Using the database, we can easily track the relationships between players, which can be utilized to build a dashboard and recommendation system.
