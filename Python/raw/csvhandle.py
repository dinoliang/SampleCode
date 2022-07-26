import time
import csv

StartTime = time.time()

#######################################################
### Change the parameters to match the settings
gCSVInputPath = '/home/dino/PythonShared/raw/Config_csv_Def-220125_reg_Default_csv.csv'
gCSVOutputPath = '/home/dino/PythonShared/raw/Config_csv_Def-220125_reg_Default_csv.csv'

#######################################################

class csvhandle:
    def __init__(self) -> None:
        pass

    def ReadCSV(self, filepath):
        with open(filepath, newline='') as csvfile:
            # Read CSV content
            rows = csv.reader(csvfile)

            for row in rows:
                print(row)
        pass

    def WriteCSV(self, filepath, OneRowInfo):
        with open(filepath, 'a+') as csvfile:
            # create the csv writer
            csv_writer = csv.writer(csvfile)

            # write a row to the csv file
            #print(OneRowInfo)
            csv_writer.writerow(OneRowInfo)
        pass

if __name__ == "__main__":
    csv_var = csvhandle()
    csv_var.ReadCSV(gCSVInputPath)
    pass

EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
