class Movie:
    def __init__(self, title, original_title, synopsis, duration, production_budget, release_date, vote_average, revenue):
        self.title = title
        self.original_title = original_title
        self.synopsis = synopsis
        self.duration = duration
        self.production_budget = production_budget
        self.release_date = release_date
        self.vote_average = vote_average
        self.revenue = revenue

        self.id = None 
        self.actors = []
        self.productors = []
        self.is_3d = None 
        self.marketing_budget = None 
        self.tmdb_id = None 


    def total_budget(self):
        if (self.production_budget == None or self.marketing_budget == None):
            return None
        return self.production_budget + self.marketing_budget
        

    

