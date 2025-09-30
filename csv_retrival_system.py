import csv 

class Analyzer_csv:
    def __init__(self, file_name: str):
        self.file = file_name
        self.n_website = {}

    def is_n_websites(self):
        with open(self.file, 'r') as r_file:
            reader_obj = csv.reader(r_file, delimiter=',')
            next(reader_obj) #skips the first field

            for i in reader_obj:
                if not i[2]:
                    self.n_website[i[0]] = i[3]
                    
    def create_list(self):
        with open(f"{self.file}_n_web.csv", 'w') as w_file:
            writer = csv.writer(w_file)

            self.is_n_websites() #create a filtered verision of the csv file with no websites 
            
            for key in self.n_website:
                writer.writerow([key, self.n_website[key]])



bhubneswar = Analyzer_csv('restaurants.csv')
bhubneswar.create_list()

