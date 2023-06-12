# Automated-data-pipeline
Uses web-scraping and APIs to create an automated data pipeline

This pipeline was created as part of the WBS CODING SCHOOL Data Science Bootcamp.

The pipeline was created to provide data for a fictional e-scooter company called Gans. Gans wants to distribute their scooters across the cities they serve in response to, among other things, the weather forecast and arrivals at nearby airports.

The pipeline uses web-scraping and API calls to gather data about cities, their populations, weather, nearby airports, and incoming flights. The data are stored in a relational database built using SQL.

The functions that retrieve data and structure it into tables are contained in modules with names beginning 'functions...'. The modules beginning with 'gans...' import the 'functions...' modules, invoke the function that creates the table, and pushes it to the SQL database.

The pipeline was hosted on AWS using RDS. EventBridge was used to schedule regular invocations of Lambda functions that updated to the weather, flights, and populations tables.

An overview of the creation of this pipeline was published on Medium.

