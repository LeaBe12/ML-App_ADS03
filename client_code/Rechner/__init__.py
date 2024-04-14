from ._anvil_designer import RechnerTemplate
from anvil import *
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables


class Rechner(RechnerTemplate):
    def __init__(self, **properties):
        # Set Form properties and Data Bindings.
        self.init_components(**properties)

        # Code zum Abrufen der Dropdown-Optionen und Setzen der Dropdown-Menüs
        self.set_dropdown_options()

    def set_dropdown_options(self):
        # Abrufen der Werte aus den Spalten 'Abschluss', 'HSU', 'Geschlecht' und 'Status' der entsprechenden Datentabellen
        abschluss_values = [r['Abschluss'] for r in app_tables.abschluss.search()]
        hsu_values = [r['HSU'] for r in app_tables.hsu.search()]
        geschlecht_values = [r['Geschlecht'] for r in app_tables.geschlecht.search()]

        # Setzen der Optionen für die Dropdown-Menüs
        self.Abschluss_dd.items = abschluss_values
        self.HSU_dd.items = hsu_values
        self.Geschlecht_dd.items = geschlecht_values
    
    def Abschluss_dd_change(self, **event_args):
        """This method is called when an item is selected"""
        pass

    def HSU_dd_change(self, **event_args):
        """This method is called when an item is selected"""
        pass

    def Geschlecht_dd_change(self, **event_args):
        """This method is called when an item is selected"""
        pass
    
    def Rechner_button_click(self, **event_args):
        """This method is called when the button is clicked"""
        # Daten aus den Dropdown-Menüs abrufen und in ein Dictionary packen
        data = {
            "Abschluss": self.Abschluss_dd.selected_value,
            "Hochschule": self.HSU_dd.selected_value,
            "Geschlecht": self.Geschlecht_dd.selected_value
        }
        
        # Serverfunktion aufrufen und das Daten-Dictionary übergeben
        predict_success = anvil.server.call('predict_success', data)
        
        # Wenn eine Kategorie zurückgegeben wird, setzen wir unsere Erfolgsprognose
        if predict_success:
            self.success_label.visible = True
            self.success_label.text = "Die Erfolgswahrscheinlichkeit der Person liegt bei {:.2%}".format(predict_success)
            self.Ausgabeicon_show()
  
    # Definiere die Methode Ausgabeicon_show, die aufgerufen wird, wenn das Label auf dem Bildschirm angezeigt wird
    def Ausgabeicon_show(self, **event_args):
        """Diese Methode wird aufgerufen, wenn das Label auf dem Bildschirm angezeigt wird"""
        # Überprüfe, ob der Text des success_label nicht leer ist
        if self.success_label.text.strip() != "":
            # Icon anzeigen, wenn der Text nicht leer ist
            self.Ausgabeicon.visible = True
        else:
            # Icon ausblenden, wenn der Text leer ist
            self.Ausgabeicon.visible = False


    