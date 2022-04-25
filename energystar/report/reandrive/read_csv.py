#!/usr/bin/env python3
import csv



if __name__ == "__main__":

    water_volume = 0
    hot_water = 0
    length = 0

    with open('march.csv', mode ='r') as file:

        reader = csv.DictReader(file)
        count = sum(1 for _ in reader)
        file.seek(0)

        # reading the CSV file
        csvFile = csv.DictReader(file)

        # displaying the contents of the CSV file
        for lines in csvFile:

            length = len(lines)
            for val in lines:
                if val == "Cold Water   (ft³)":

                    water_volume = water_volume + float(lines[val])
                elif(val == "Pool Water   (m³)") or (val == "Spa water meter   (m³)"):

                    volume = float(lines[val]) * 35.3146667

                    water_volume = water_volume + volume

                elif val == "Hot Water   (ft³)":

                    hot_water = hot_water + float(lines[val])



    hot_water_volume = hot_water - (100*24*(count-1))
    print(f"water_volume = {water_volume},  hot_water = {hot_water} , {hot_water_volume}, {count}")
