import json
import pandas as pd
import plotly.express as px


# Klasse EKG-Data für Peakfinder, die uns ermöglicht peaks zu finden

class EKGdata:

    @staticmethod
    def load_ekg_data_by_id(ekg_liste, search_id):
        ekg_dict = EKGdata.load_ekg_data()
        if search_id == "None":
            return {1: "No ID given"}
        
        for ekg_dict in ekg_liste:
            if ekg_dict["id"] == search_id:
                #print(ekg_dict)
                return ekg_dict
        else:
            return {1: "No EKG with this ID found"}
        
    @staticmethod
    def load_ekg_data():
        """A Function that knows where te person Database is and returns a Dictionary with the Persons"""
        file = open("data/person_db.json")
        ekg_data = json.load(file)
        return ekg_data

## Konstruktor der Klasse soll die Daten einlesen

    def __init__(self, ekg_dict):
        #pass
        self.id = ekg_dict["id"]
        self.date = ekg_dict["date"]
        self.data = ekg_dict["result_link"]
        self.df = pd.read_csv(self.data, sep='\t', header=None, names=['Messwerte in mV','Zeit in ms',])
        self.df = self.df.iloc[:5000]  # Entferne die erste Zeile, da sie nur die Spaltennamen enthält
        self.peaks = []


    def find_peaks(self, threshold, respacing_factor=5):

        self.series = self.df['Messwerte in mV']
    # Respace the series
        self.series = self.series.iloc[::respacing_factor]
    
    # Filter the series
        self.series = self.series[self.series>threshold]

        last = 0
        current = 0
        next = 0

        for index, row in self.series.items():
            last = current
            current = next
            next = row

            if last < current and current > next and current > threshold:
                self.peaks.append(index-respacing_factor)

        return self.peaks
    
    
    def plot_time_series(self):

        # Erstellte einen Line Plot, der ersten 2000 Werte mit der Zeit aus der x-Achse
        self.fig = px.line(self.df.head(2000), x="Zeit in ms", y="Messwerte in mV")
        #return self.fig

if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_liste = person_data[0]["ekg_tests"]

    ekg_dict = EKGdata.load_ekg_data_by_id(ekg_liste, 2)
    print(ekg_dict)
    ekg = EKGdata(ekg_dict)
    peaks = ekg.find_peaks(threshold=240)
    print(peaks)