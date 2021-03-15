import csv
import os


def WriteCarSpectoFile(car_path, car_specs):
    with open(os.path.join(car_path,'car_spec_file.csv'), 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=';', quotechar='"')

        for key,value in car_specs.items():
            spamwriter.writerow([key,value])


