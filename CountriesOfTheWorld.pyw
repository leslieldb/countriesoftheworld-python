import sys
import csv
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap

#ADD IMPORT STATEMENT FOR YOUR GENERATED UI.PY FILE HERE
import Ui_CountriesOfTheWorld
#      ^^^^^^^^^^^ Change this!

#CHANGE THE SECOND PARAMETER (Ui_ChangeMe) TO MATCH YOUR GENERATED UI.PY FILE
class MyForm(QMainWindow, Ui_CountriesOfTheWorld.Ui_MainWindow):
#                         ^^^^^^^^^^^   Change this!

    #GLOBAL VARIABLES - Used in multiple functions
    CountryDataList = []
    CountryPopulationList = []
    TotalWorldPopulation = 0
    CurrentPopulationDensityMiles = 0
    CurrentPopulationDensityKMs = 0
    CountryAreaMiles = 0
    CountryAreaKMs = 0
    fileName = "files\\countries.txt"

    # DO NOT MODIFY THIS CODE
    def __init__(self, parent=None):
        super(MyForm, self).__init__(parent)
        self.setupUi(self)
    # END DO NOT MODIFY

        # ADD SLOTS HERE, indented to this level (ie. inside def __init__)
        self.frameCountryContent.setVisible(False)
        self.actionSave_To_File.setEnabled(False)

        self.actionLoad_Countries.triggered.connect(self.LoadCountries_Triggered)
        self.listWidgetCountries.currentRowChanged.connect(self.ListIndex_Changed)
        self.pushButtonUpdatePopulation.clicked.connect(self.UpdateButton_Clicked)
        self.actionSave_To_File.triggered.connect(self.SaveToFile_Triggered)
        self.actionExit.triggered.connect(self.Exit_Triggered)
        self.comboBoxAreaUnits.currentIndexChanged.connect(self.AreaComboBox_Changed)
        self.radioButtonSquareMile.clicked.connect(self.RadioSqMile_Clicked)
        self.radioButtonSquareKilometer.clicked.connect(self.RadioSqKMs_Clicked)


    # ADD SLOT FUNCTIONS HERE
    # These are the functions your slots will point to
    # Indent to this level (ie. inside the class, at same level as def __init__)

    def LoadCountries_Triggered(self):

        #Loads all data from file into 2D list
        self.LoadCountriesFromFile()

        #Loads the countries list widget
        self.LoadCountriesListBox()

        #Calculates total population of all countries
        self.CalculateTotalWorldPopulation()

        #Disable the load countries button, as the file is no different at this time
        self.actionLoad_Countries.setEnabled(False)
        #Show the frame of content
        self.frameCountryContent.setVisible(False)

    def ListIndex_Changed(self):
        #If the frame isn't being shown, show the frame
        if self.frameCountryContent.isVisible() == False:
            self.frameCountryContent.setVisible(True)

        #Take the current selected index in the list widget, and store in a variable
        selectedIndex = self.listWidgetCountries.currentRow()

        #Display the currently selected country's data
        self.DisplayCountryData(selectedIndex)

    def UpdateButton_Clicked(self):

        #Take the current selected index in the list widget, and store in a variable
        selectedIndex = self.listWidgetCountries.currentRow()

        #Take the text from the line edit and store in variable
        NewCountryPopulation = (self.lineEditPopulationNum.text())

        #Remove the comma and space notation from the number so it can be converted to an integer
        NewCountryPopulation = NewCountryPopulation.replace(",", "")
        NewCountryPopulation = NewCountryPopulation.replace(" ", "")

        #Data validation - country population has to be a whole number
        try:
            NewCountryPopulation = int(NewCountryPopulation)
        except ValueError:
            #If data is invalid, popup telling user that it is invalid, then kick them out of the function
            QMessageBox.information(self, "Error", "Population input was invalid.", QMessageBox.Ok)
            return
        
        #Send the country's new population to the global data list, overwriting the old one
        self.CountryDataList[selectedIndex][1] = NewCountryPopulation

        #Calculate the new total population
        self.CalculateTotalWorldPopulation()

        #Popup telling user that the population has been updated successfully in memory
        QMessageBox.information(self, "Successful", "Population was updated successfully, but has not been saved.", QMessageBox.Ok)

        #Display the updated country data in content frame
        self.DisplayCountryData(selectedIndex)
        
        #If load countries button is disabled, re-enable, as the file is now different, and the user may want to reload
        if self.actionLoad_Countries.isEnabled() == False:
            self.actionLoad_Countries.setEnabled(True)
        
        #Enable the save button, as there are now unsaved changes
        self.actionSave_To_File.setEnabled(True)

    def AreaComboBox_Changed(self):
        
        #Display country's area in either miles or kilometers, depending on whats selected in the combo box
        if self.comboBoxAreaUnits.currentIndex() == 0:
            #If miles (index 0) is selected, display in square miles, to 1 decimal place
            self.labelAreaNum.setText("{0:,.1f}".format(self.CountryAreaMiles))
        elif self.comboBoxAreaUnits.currentIndex() == 1:
            #If kilometers (index 1) is selected, display in square kilometers, to 1 decimal place
            self.labelAreaNum.setText("{0:,.1f}".format(self.CountryAreaKMs))

    def RadioSqMile_Clicked(self):
        #Displays population density per square mile, to 2 decimal places, with comma notation
        self.labelDensityNum.setText("{0:,.2f}".format(self.CurrentPopulationDensityMiles))

    def RadioSqKMs_Clicked(self):
        #Displays population density per square kilometer, to 2 decimal places, with comma notation
        self.labelDensityNum.setText("{0:,.2f}".format(self.CurrentPopulationDensityKMs))

    def SaveToFile_Triggered(self):
        #Writes data to file, if save button is clicked
        self.SaveCountriesToFile()

    def Exit_Triggered(self):

        #If there are unsaved changes, ask user if they want to save before exiting
        if self.actionSave_To_File.isEnabled() == True:
            reply = QMessageBox.question(self, "Save", "Save changes to file before closing?", QMessageBox.Yes, QMessageBox.No)
            #If they say yes, run save function
            if reply == QMessageBox.Yes:
                self.SaveCountriesToFile()

        #Exit program
        QApplication.closeAllWindows()

    #ADD HELPER FUNCTIONS HERE
    # These are the functions the slot functions will call, to 
    # contain the custom code that you'll write to make your progam work.
    # Indent to this level (ie. inside the class, at same level as def __init__)

    def LoadCountriesFromFile(self):
        #Reads file as CSV
        accessMode = "r"
        myFile = open(self.fileName, accessMode)

        fileData = csv.reader(myFile)
        
        #Clears 2d list, as new file is loaded
        self.CountryDataList.clear()

        #Adds all data to 2D list, then closes file
        for row in fileData:
            self.CountryDataList.append(row)

        myFile.close()

    def LoadCountriesListBox(self):

        #Clears the List Widget, as new countries are being loaded
        self.listWidgetCountries.clear()

        #Adds the country names to List Widget as options
        for row in self.CountryDataList:
            self.listWidgetCountries.addItem(row[0])
    
    def CalculateTotalWorldPopulation(self):
        #Clears population global list
        self.CountryPopulationList.clear()

        #Appends all country populations to a new global list, as integers
        for row in self.CountryDataList:
            self.CountryPopulationList.append(int(row[1]))
        
        #Adds together all country populations and stores in a new variable
        self.TotalWorldPopulation = sum(self.CountryPopulationList)

    def DisplayCountryData(self, selectedIndex):
        #Takes country name, population, and area from 2D list and stores in their own variables
        CountryName = self.CountryDataList[selectedIndex][0]
        CountryPopulation = int(self.CountryDataList[selectedIndex][1])
        self.CountryAreaMiles = float(self.CountryDataList[selectedIndex][2])

        #Converts the country area from square miles to square kilometers, and stores in its own variable
        self.CountryAreaKMs = (self.CountryAreaMiles * 2.58998811)

        #Sets the file name of the country's flag
        CountryFlagFileName = CountryName.replace(" ", "_")
        CurrentFlag = QPixmap("files\\Flags\\" + CountryFlagFileName + ".png")

        #Calculates country's world population percentage
        CurrentPopulationPercentage = ((CountryPopulation / self.TotalWorldPopulation) * 100)

        #Calculates population density in miles and kilometers
        self.CurrentPopulationDensityMiles = (CountryPopulation / self.CountryAreaMiles)
        self.CurrentPopulationDensityKMs = (CountryPopulation / self.CountryAreaKMs)

        #Sets the top label to the country name
        self.labelCountryName.setText(CountryName)

        #Sets the line edit to the population, to no decimal places, with comma notation
        self.lineEditPopulationNum.setText("{0:,.0f}".format(CountryPopulation))

        #Sets area label to the country area in miles, with comma notation
        self.labelAreaNum.setText("{0:,}".format(self.CountryAreaMiles))

        #Sets flag label to display the country's flag
        self.labelCountryFlagImage.setPixmap(CurrentFlag)

        #Sets percentage label to display the country's world population percentage, to 4 decimal places
        self.labelPercentageNum.setText("{0:.4f}%".format(CurrentPopulationPercentage))

        #Sets density label to display country's population density
        if self.radioButtonSquareKilometer.isChecked() == True:
            #If KMs radio button is clicked, automatically displays density in KMS
            self.labelDensityNum.setText("{0:.2f}".format(self.CurrentPopulationDensityKMs))
        else:
            #If Miles radio button is clicked, automatically displays density in miles
            self.labelDensityNum.setText("{0:.2f}".format(self.CurrentPopulationDensityMiles))

    def SaveCountriesToFile(self):
        #Opens file to overwrite and save
        accessMode = "w"
        myFile = open(self.fileName, accessMode)

        #Writes every index to file in order, separated by commas
        for row in range(len(self.CountryDataList)):
            myFile.write(self.CountryDataList[row][0] + ",")
            myFile.write(str(self.CountryDataList[row][1]) + ",")
            myFile.write(str(self.CountryDataList[row][2]))
            #Detects if there will be a new line, and writes a new line if there is
            if (row + 1) in (range(len(self.CountryDataList))):
                myFile.write("\n")

        #Popup box to alert user that the save was successful
        QMessageBox.information(self, "Successful", "Data was saved to file successfully.", QMessageBox.Ok)

        #Closes file
        myFile.close()

        #Disables the save button, as no unsaved changes exist at this time
        self.actionSave_To_File.setEnabled(False)

#   Example Helper Function
#   def Save(self):
#       Implement the save functionality here

# DO NOT MODIFY THIS CODE
if __name__ == "__main__":
    app = QApplication(sys.argv)
    the_form = MyForm()
    the_form.show()
    sys.exit(app.exec_())
# END DO NOT MODIFY