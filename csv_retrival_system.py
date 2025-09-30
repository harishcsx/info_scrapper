import csv 

class Analyzer_csv:
    def __init__(self, file_name: str):
        self.file = file_name
        self.n_website = {}

    def is_n_websites(self):
        count = 0

        with open(self.file, 'r') as file:
            reader_obj = csv.reader(file, delimiter=',')
            next(reader_obj) #skips the first field

            for i in reader_obj:
                if not i[2]:
                    self.n_website[i[0]] = i
                    count += 1

            print("stores not having websites : ", count)

    def list_n_websites(self):
        for idx, item in enumerate(self.n_website):
            print(f"store {idx+1} : ", item)




bhubneswar = Analyzer_csv('restaurants.csv')
bhubneswar.is_n_websites()
bhubneswar.list_n_websites()

