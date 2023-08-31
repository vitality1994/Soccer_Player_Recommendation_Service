## How to decide what type of database should be used?
[reference video (Korean)](https://www.youtube.com/watch?v=ZVuHZ2Fjkl4)

### Types of databases

<br/>

1. Key-value Database
    * good to use for caching (place to copy data or value temporary)
2. Relational Database
    * for matrix table format
    * sql language
    * data normalization required → many tables required
    * ACID transaction (good for money transaction)
    * good to use when accuracy is the most important
3. Graph Database
    * ave data in node
    * save relationship between node
    * ex, location of airplanes, relationship between people (facebook), recommendation system
4. Document Database
    * save a json file
    * no need to care about columns
    * no need normalization
    * good for parallization 
    * accuracy could be worse
5. Column-family Database
    * no need to have fixed columns for each raw
    * no need normalization
    * accuracy could be worse
    * good for copy, parallization