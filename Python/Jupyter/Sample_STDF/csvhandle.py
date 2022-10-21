import time
import csv
import numpy as np

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
            csvrows = csv.reader(csvfile, delimiter=',')

            rows = []
            for row in csvrows:
                rows.append(row)
            #print(rows)
        return rows

    def ReadCSV(self, filepath, nBeginColumn):
        with open(filepath, newline='') as csvfile:
            # Read CSV content
            csvrows = csv.reader(csvfile, delimiter=',')

            rows = []
            nRow = 0
            for row in csvrows:
                if nRow < nBeginColumn:
                    nRow = nRow + 1
                    continue
                rows.append(row)
            #print(rows)
        return rows

    def WriteCSV_OneRow(self, filepath, mode, OneRowInfo):
        with open(filepath, mode, newline='') as csvfile:   # ex: mode = 'a+'
            # create the csv writer
            csv_writer = csv.writer(csvfile, delimiter=',')

            # write a row to the csv file
            #print(OneRowInfo)
            csv_writer.writerow(OneRowInfo)
        pass

    def WriteCSV_Rows(self, filepath, mode, RowsInfo):
        with open(filepath, mode, newline='') as csvfile:   # ex: mode = 'a+'
            # create the csv writer
            csv_writer = csv.writer(csvfile, delimiter=',')

            # write a row to the csv file
            #print(OneRowInfo)
            csv_writer.writerows(RowsInfo)
        pass

    def ReadCSVToNumpy(self, filepath):
        rows = np.genfromtxt(filepath, delimiter=',')
        print(rows)
        return rows

    def WriteCSVToNumpy(self, filepath, array):
        rows = np.savetxt(filepath, array, delimiter=',', fmt='%d')
        return

if __name__ == "__main__":
    csv_var = csvhandle()
    csv_var.ReadCSV(gCSVInputPath)
    pass

EndTime = time.time()
print("Durning Program Time(sec): ", EndTime - StartTime)
