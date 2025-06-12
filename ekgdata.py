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
        self.fig = px.line(self.df.head(10000), x="Zeit in ms", y="Messwerte in mV")
        #return self.fig


    def estimate_heart_rate(self):
        """Eine Funktion, die die Herzfrequenz schätzt"""
        if len(self.peaks) < 2:
            return "Not enough peaks found to estimate heart rate"
        
        # Berechne die Zeitdifferenz zwischen den Peaks
        peak_intervals = [self.peaks[i+1] - self.peaks[i] for i in range(len(self.peaks)-1)]
        
        # Durchschnittliche Zeit zwischen den Peaks
        avg_interval = sum(peak_intervals) / len(peak_intervals)  # in Sekunden
        
        # Herzfrequenz in bpm (Beats per Minute)
        heart_rate1 = 60000 / avg_interval
        heart_rate2 = heart_rate1 / 6  # in Beats per Minute (bpm)

        return heart_rate2
    
    def plot_time_series_with_peaks(self, peaks):
        self.plot_time_series()  # Basis-Zeitreihe zeichnen

    # Extrahiere die Zeit- und Messwerte der Peaks anhand der Indizes
        peak_zeiten = self.df['Zeit in ms'].iloc[peaks]
        peak_werte = self.df['Messwerte in mV'].iloc[peaks]

    # Peaks als rote Punkte hinzufügen
        self.fig.add_scatter(
            x=peak_zeiten,
            y=peak_werte,
            mode='markers',
            name='Peaks',
            marker=dict(color='red', size=8)
        )
        fig3 = self.fig
        return fig3



if __name__ == "__main__":
    file = open("data/person_db.json")
    person_data = json.load(file)
    ekg_liste = person_data[0]["ekg_tests"]

    ekg_dict = EKGdata.load_ekg_data_by_id(ekg_liste, 2)

    ekg = EKGdata(ekg_dict)
    peaks = ekg.find_peaks(threshold=240)
    estimatehr = ekg.estimate_heart_rate()
    