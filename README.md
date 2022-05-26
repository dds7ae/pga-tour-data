# PGA Tour Data

# Environment Setup
1. Install Python 3. I'm using 3.0
2. Use Pycharm if it makes it easier
3. Add the modules in `pga_scraper.py` if they are not installed either via `pip3 install x` or your Pycharm.
4. Make sure the tags in `pga_scraper.py` are still accurate to the HTML just do a simple inspect and see the pattern.
5. Edit the years if necessary then run `pga_scraper.py`
6. Then you should get `pga_tour_data.csv.csv`
7. 
`pga_tour_data.csv.csv`Each row indicates a golfer's performance for that year.

* Player Name: Name of the golfer
* Rounds: The number of games that a player played
* Fairway Percentage: The percentage of time a tee shot lands on the fairway
* Year: The year in which the statistic was collected
* Avg Distance: The average distance of the tee-shot
* gir: (Green in Regulation) is met if any part of the ball is touching the putting surface while the number of strokes taken is at least two fewer than par
* Average Putts: The average number of strokes taken on the green
* Average Scrambling: Scrambling is when a player misses the green in regulation, but still makes par or better on a hole
* Average Score: Average Score is the average of all the scores a player has played in that year
* Points: The number of FedExCup points a player earned in that year. These points can be earned by competing in tournaments.
* Wins: The number of competition a player has won in that year
* Top 10: The number of competitions where a player has placed in the Top 10
* Average SG Putts: Strokes gained: putting measures how many strokes a player gains (or loses) on the greens.
* Average SG Total: The Off-the-tee + approach-the-green + around-the-green + putting statistics combined
* SG:OTT: Strokes gained: off-the-tee measures player performance off the tee on all par-4s and par-5s.
* SG:APR: Strokes gained: approach-the-green measures player performance on approach shots. Approach shots include all shots that are not from the tee on par-4 and par-5 holes and are not included in strokes gained: around-the-green and strokes gained: putting. Approach shots include tee shots on par-3s.
* SG:ARG: Strokes gained: around-the-green measures player performance on any shot within 30 yards of the edge of the green. This statistic does not include any shots taken on the putting green.
* Money: The amount of prize money a player has earned from tournaments
* The official explanation for strokes gained is included [here](https://www.pgatour.com/news/2016/05/31/strokes-gained-defined.html).