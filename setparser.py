import argparse

class Parser:


    def set_parser(self):

        parser = argparse.ArgumentParser(description='Process MoviePredictor data')
        parser.add_argument('context', choices=['people', 'movies'], help='Le contexte dans lequel nous allons travailler')
        action_subparser = parser.add_subparsers(title='action', dest='action')


        # [movies,people] list 
        list_parser = action_subparser.add_parser('list', help='Liste les entitées du contexte')
        list_parser.add_argument('--export' , help='Chemin du fichier exporté')

        # [movies,people] find id 
        find_parser = action_subparser.add_parser('find', help='Trouve une entité selon un parametre')
        find_parser.add_argument('id' , help='Identifant Ã  rechercher')

        insert_parser = action_subparser.add_parser('insert', help='Insere une entité dans la database')
        scrap_parser = action_subparser.add_parser('scrap', help='scrap les infos d\'un film sur Wikipedia')

        #  movies import --file newfile.csv
        import_parser = action_subparser.add_parser('import', help='importer un film dans la DB')



        know_args = parser.parse_known_args()[0]
        if know_args.context == "people":
            # [movies,people] insert [title,duration,orginal-title,rating,release-date,synopsis,production-budget, marketing-budget|firstname,lastname]
            insert_parser.add_argument('--firstname', help='Prénom', required=True)
            insert_parser.add_argument('--lastname', help='Nom de famille', required=True)

        if know_args.context == "movies":
            insert_parser.add_argument('--title', help='Titre', required=True)
            insert_parser.add_argument('--original-title', help='Titre original', required=True)
            insert_parser.add_argument('--synopsis', help='Synopsis', required=True)
            insert_parser.add_argument('--duration', help='Durée du film', required=True)
            insert_parser.add_argument('--production-budget', help='Budget production', required=True)
            insert_parser.add_argument('--release-date', help='Date de sortie', required=True)
            insert_parser.add_argument('--marketing-budget', help='Budget Marketing', required=True)
            insert_parser.add_argument('--vote_average', help='Date de sortie', required=True)
            insert_parser.add_argument('--revenue', help='Date de sortie', required=True)

            # movies scrap URL fiche film Wiki

            scrap_parser.add_argument('url', help='url de la page wiki à scraper')

            # movies import --api themoviedb --tmdbId 785

            import_parser.add_argument('--file' , help='file.csv')
            import_parser.add_argument('--api' , help='Api utilisé pour importer des films')
            import_parser.add_argument('--year' , help='films de l\'année year avec + de 4000 votes')
            import_parser.add_argument('--tmdbId' , help='Id du film tmdb')

        args = parser.parse_args()
        return args