import streamlit as st
import pickle
from datetime import date
from PIL import Image
from lightgbm import LGBMClassifier

model_filename = 'Model & Scalers/LGBM.pkl'
model = pickle.load(open(model_filename, 'rb'))
cat_encoder_filename = 'Model & Scalers/cat_encoder.pkl'
cat_encoder = pickle.load(open(cat_encoder_filename, 'rb'))
num_scaler_filename = 'Model & Scalers/num_encoder.pkl'
num_scaler = pickle.load(open(num_scaler_filename, 'rb'))

logo = 'others\logo.png'
st.image(Image.open(logo))

st.text("")
st.text("")

st.write("Ingrese los siguientes datos para efectuar su reserva")

hoteles = ['BLESS HOTEL IBIZA',
           'BLESS HOTEL MADRID',
           'DOMINICAN FIESTA HOTEL & CASINO',
           'FIESTA HOTEL CALA GRACIO',
           'FIESTA HOTEL TANIT',
           'GRAND PALLADIUM BAVARO HOTEL',
           'GRAND PALLADIUM COLONIAL',
           'GRAND PALLADIUM COSTA MUJERES',
           'GRAND PALLADIUM GARDEN BEACH',
           'GRAND PALLADIUM IMBASSAI',
           'GRAND PALLADIUM JAMAICA RESORT & SPA',
           'GRAND PALLADIUM KANTENAH',
           'GRAND PALLADIUM LADY HAMILTON RESORT & SPA',
           'GRAND PALLADIUM PALACE HOTEL',
           'GRAND PALLADIUM PALACE IBIZA',
           'GRAND PALLADIUM PUNTA CANA HOTEL',
           'GRAND PALLADIUM SICILIA RESORT & SPA HOTEL',
           'GRAND PALLADIUM VALLARTA',
           'GRAND PALLADIUM WHITE SAND',
           'GRAND PALLADIUM┬á WHITE ISLAND',
           'HARD ROCK HOTEL IBIZA',
           'HARD ROCK HOTEL TENERIFE',
           'AGROTURISMO SA TALAIA',
           'PALLADIUM CALA LLONGA HOTEL',
           'PALLADIUM COSTA DEL SOL',
           'PALLADIUM DON CARLOS HOTEL',
           'PALLADIUM HOTEL PALMYRA',
           'PALLADIUM MENORCA',
           'TRS CAP CANA HOTEL',
           'TRS CORAL HOTEL',
           'TRS TURQUESA HOTEL',
           'TRS YUCATAN HOTEL',
           'USHUAIA BEACH HOTEL']

Hotel = st.selectbox("Seleccione hotel", options=hoteles)
check_in = st.date_input("Fecha del entrada")
check_out = st.date_input("Fecha del salida")
n_dias = (check_in - date(2021, 9, 30)).days
n_noches = (check_out - check_in).days
n_adultos = st.slider("Número de adultos", 0, 10, 1)
n_ninos = st.slider("Número de niños", 0, 10, 0)
n_bebes = st.slider("Número de bebés", 0, 10, 0)
regimen = st.selectbox("Régimen: ", options=['Todo incluido', 'Media pensión', 'Sólo desayuno', 'Ninguno'])

marcas = {'BLESS HOTEL IBIZA': 'BLESS',
          'BLESS HOTEL MADRID': 'BLESS',
          'DOMINICAN FIESTA HOTEL & CASINO': 'FIESTA',
          'FIESTA HOTEL CALA GRACIO': 'FIESTA',
          'FIESTA HOTEL TANIT': 'FIESTA',
          'GRAND PALLADIUM BAVARO HOTEL': 'GRAND PALLADIUM',
          'GRAND PALLADIUM COLONIAL': 'GRAND PALLADIUM',
          'GRAND PALLADIUM COSTA MUJERES': 'GRAND PALLADIUM',
          'GRAND PALLADIUM GARDEN BEACH': 'GRAND PALLADIUM',
          'GRAND PALLADIUM IMBASSAI': 'GRAND PALLADIUM',
          'GRAND PALLADIUM JAMAICA RESORT & SPA': 'GRAND PALLADIUM',
          'GRAND PALLADIUM KANTENAH': 'GRAND PALLADIUM',
          'GRAND PALLADIUM LADY HAMILTON RESORT & SPA': 'GRAND PALLADIUM',
          'GRAND PALLADIUM PALACE HOTEL': 'GRAND PALLADIUM',
          'GRAND PALLADIUM PALACE IBIZA': 'GRAND PALLADIUM',
          'GRAND PALLADIUM PUNTA CANA HOTEL': 'GRAND PALLADIUM',
          'GRAND PALLADIUM SICILIA RESORT & SPA HOTEL': 'GRAND PALLADIUM',
          'GRAND PALLADIUM VALLARTA': 'GRAND PALLADIUM',
          'GRAND PALLADIUM WHITE SAND': 'GRAND PALLADIUM',
          'GRAND PALLADIUM┬á WHITE ISLAND': 'GRAND PALLADIUM',
          'HARD ROCK HOTEL IBIZA': 'HARD ROCK',
          'HARD ROCK HOTEL TENERIFE': 'HARD ROCK',
          'AGROTURISMO SA TALAIA': 'HOTEL BOUTIQUE',
          'PALLADIUM CALA LLONGA HOTEL': 'PALLADIUM',
          'PALLADIUM COSTA DEL SOL': 'PALLADIUM',
          'PALLADIUM DON CARLOS HOTEL': 'PALLADIUM',
          'PALLADIUM HOTEL PALMYRA': 'PALLADIUM',
          'PALLADIUM MENORCA': 'PALLADIUM',
          'TRS CAP CANA HOTEL': 'TRS',
          'TRS CORAL HOTEL': 'TRS',
          'TRS TURQUESA HOTEL': 'TRS',
          'TRS YUCATAN HOTEL': 'TRS',
          'USHUAIA BEACH HOTEL': 'USHUAIA',
          }

marca = marcas[Hotel]

if n_dias in range(0, 4, 1):
    lead_time = '0-3'
elif n_dias in range(4, 8, 1):
    lead_time = '4-7'
elif n_dias in range(8, 16, 1):
    lead_time = '8-15'
elif n_dias in range(16, 31, 1):
    lead_time = '16-30'
elif n_dias in range(30, 91, 1):
    lead_time = '30-90'
elif n_dias in range(90, 181, 1):
    lead_time = '90-180'
else:
    lead_time = '+180'

t_reserva = 'DESCONOCIDO'
pais = 'ESPAÑA'
fuente = 'DESCONOCIDA'

all_inclusive = 1 if regimen == 'Todo incluido' else 0

categoricas = [marca, t_reserva, lead_time, pais, fuente]

marca, t_reserva, lead_time, pais, fuente = cat_encoder.transform(categoricas)
n_noches = num_scaler.transform(n_noches)

X = [marca, 0, 0, t_reserva, n_noches, lead_time, n_adultos, n_ninos, n_bebes, pais, 0, fuente, 1, 1, all_inclusive, 1, 0]
prediction = model.predict(X)

st.write('Su reserva ha sido procesada correctamente, aunque no contamos con que aparezca :(') if prediction[0] == 1 else st.write('Su reserva ha sido procesada correctamente, le esperamos :)')
