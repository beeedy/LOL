import urllib2
import simplejson
import time
from BeautifulSoup import BeautifulSoup

allGames = []
lastGame = []

def compare_games(game1, game2):
	# returns true if the two game are the same, otherwise false
	game1 = [name for teams in game1 for player in teams for name in player]
	game2 = [name for teams in game2 for player in teams for name in player]

	if len(game1) != len(game2):
		return False

	for i in range(len(game1)):
		if game1[i] != game2[i]:
			return False
	return True


try:
	with open('aramGames.txt', 'r') as gameFile:
		allGames = simplejson.load(gameFile)
		lastGame = allGames[-1]
except:
	print("Could not find list of previously recorded games, making new file now...")

while True:
	#this is the URL for lolnexus' most recent ARAM's 
	games = []
	num1game = []

	for i in range(1, 5):
		# get games from all the pages!
		soup = BeautifulSoup(urllib2.urlopen("http://www.lolnexus.com/recent-games?filter-region=1&filter-game-map=7&filter-queue-type=12&filter-sort=2&page={}".format(i)))
		tempGames = soup.body.findAll('div', {'class' : 'game-body'})
		for temp in tempGames:
			games.append(temp)

	print("Checking for new games...")
	for i in range(len(games)):
		game = games[i]
		team1 = game.findAll('div', {'class' : 'team-1'})[0]
		team2 = game.findAll('div', {'class' : 'team-2'})[0]
		team1 = [[a.i['title'], a.h4.findAll(text=True)[0]] for a in team1.findAll('div', {'class' : 'player'})]
		team2 = [[a.i['title'], a.h4.findAll(text=True)[0]] for a in team2.findAll('div', {'class' : 'player'})]
		teams = [team1, team2]

		if i == 0:
			# this is the most recent game, record it so we know when to stop next time
			num1game = teams

		if not compare_games(teams, lastGame):
			# make sure we don't already have this game recorded
			allGames.append(teams)
		else:
			break

		print("Recorded new game! Currently saved {} games".format(len(allGames)))

	lastGame = num1game

	with open('aramGames.txt', 'w') as gameFile:
		simplejson.dump(allGames, gameFile)

	time.sleep(20)
