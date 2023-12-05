from crawlers.league_of_graph import LeagueOfGraph

if __name__ == '__main__':
    log = LeagueOfGraph()
    result = log.matchups_page(
        champion='amumu', lane='jg').get_matchups_best_with()
    print(result)
