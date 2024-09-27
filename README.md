# 4153-user-interactions
The User Interaction Service is responsible for managing user interactions with recipes, such as liking recipes, commenting on recipes, and following other users. This service is part of a larger recipe sharing platform and integrates with the MySQL database to store and retrieve interaction data.

We chose MySQL because it effectively handles structured, relational data like user interactions (likes, comments, follows), and AWS manages it through Amazon RDS (Relational Database Service), providing automated backups, scaling, and maintenance.