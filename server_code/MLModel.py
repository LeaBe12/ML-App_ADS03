import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import pandas as pd
import xlrd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LogisticRegression
import anvil.tables.query as q


@anvil.server.callable
def return_data_from_excel():
    # Lade die Excel-Datei aus den Data Files
    with open(data_files['Daten.xlsx'], "rb") as f:
        # Lese die Daten mit Pandas
        df = pd.read_excel(f, engine='openpyxl')
    return df
data = return_data_from_excel()

# Splitten der Daten
X = data[["Abschluss", "Hochschule", "Geschlecht"]]
y = data["Erfolgreich"]

# Encoden der Daten
encoder = OneHotEncoder()
X_encoded = encoder.fit_transform(X).toarray()

# Splitten in Training- und Testset
X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.1, random_state=42)

# Initialisierung und Training
model = LogisticRegression(max_iter=1000)
model.fit(X_train, y_train)


@anvil.server.callable
def predict_success(data):
    # Daten in DataFrame konvertieren
    new_data = pd.DataFrame(data, index=[0])
    # Kodieren der kategorialen Spalten
    new_data_encoded = encoder.transform(new_data).toarray()
    # Vorhersage der Erfolgswahrscheinlichkeit
    prediction = model.predict_proba(new_data_encoded)[:, 1]  # Erfolgswahrscheinlichkeit
    return prediction[0]

# Beispielaufruf zum Testen
example_data = {
    "Abschluss": ["Bachelor"],
    "Hochschule": ["UHH"],
    "Geschlecht": ["männlich"]
}
print("Erfolgswahrscheinlichkeit:", predict_success(example_data))
