import streamlit as st
import pandas as pd
import numpy as np
import requests
import plotly_express as px
import plotly.graph_objects as go
import copy
import math
from urllib.request import urlopen
import json
import re
import time
import os.path

st.title('Web app Mon Compte Formation')

# Liste de toutes les formations qui nous intéressent
formations = ["dessinateur btp",
              "infographiste",
              "developpeur web",
              "developpeur web mobile",
              "web",
              "web 2.0",
              'web Designer',
              'referenceur web',
              "programmation web",
              "concepteur developpeur d'applications",
              "java",
              "autocad",
              "revit",
              "archicad",
              "sketchup",
              "artlantis",
              "3ds max",
              "solidworks",
              "inventor",
              "photoshop",
              "illustrator",
              "indesign",
              "after effects",
              "premiere pro",
              "4D",
              "light room",
              "wordpress",
              "html",
              "css",
              "prestashop",
              "referencement web",
              "gestionnaire media sociaux",
              "community management",
              "webmarketing",
              "seo",
              "newsletter",
              "cybersecurite",
              "animateur communautes web",
              "redacteur web",
              "administration site web",
              "site internet",
              "infographie web",
              "ui ux designer",
              "e commerce",
              "office word excel powerpoint ",
              "pcie",
              "clea numerique"]

# Quadrillage de la France
cities = ["44000", "75001", "33000", "69001", "72000", "13001", "54000", "59000",
           "31000", "87000", "18000","20000","10000","14000","35000","80000",
           "37000","21000","67000","17000","63000","38000","06000","34000",
           "64100","15000"]

@st.cache(suppress_st_warning=True)
def load_data(formations):
    with st.spinner('Please wait : the app is loading data from www.moncompteformation.gouv.fr'):
        all_form = {}
        frames = {}
        formations_new = []

        headers = {
            'authority': 'www.moncompteformation.gouv.fr',
            'accept': 'application/json, text/plain, */*',
            'origin': 'https://www.moncompteformation.gouv.fr',
            'x-xsrf-token': 'aaeeaab6-8806-4969-a2aa-a614eb26839c',
            'x-requestid': '38ea305b-56f1-8345-746a-90d5960dc94c',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
            'content-type': 'application/json',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'referer': 'https://www.moncompteformation.gouv.fr/espace-prive/html/',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': 'JSESSIONID=AEC772680A78C76FF000587B14DE2BF4.xsl6eihm_b4; visid_incap_249257=+Zy/6afORoiAX7OEdT3tms/d1l0AAAAAQUIPAAAAAADLezLhGsc7K6ZSaNLdKcpW; incap_ses_878_249257=YnlZWvllrCdj8HLuT0kvDNDd1l0AAAAA+BLv453AQLioH7tO0D1H7w==; incap_ses_474_249257=05ksAOjsCGxSKxTw+v2TBkHe1l0AAAAASnhsVWmYkPtr2cClG5mS/A==; incap_ses_727_249257=SVlUOKnGKAh/RLKb29MWCnXe1l0AAAAAOBs3mEdluJigWM9RBEvx3g==; incap_ses_245_249257=fkuKdY/k3BcbYi0pL2tmA/jk1l0AAAAA5xw4B1M3evgaejdVjuZNJw==; incap_ses_533_249257=K84ZCjjz4lMgE8jrS7JlB37l1l0AAAAA/Xd4ul5uctJScG9078solQ==; incap_ses_535_249257=2puXA1rjWFVQy+eV3bNsB37l1l0AAAAAIuYog7R2LXaAW9I6l65y5A==; incap_ses_875_249257=1XagYUSpcS8cGohN5KAkDH7l1l0AAAAAwRgz1z///KC5zwuwCrkFjg==; incap_ses_473_249257=D/nODwA8Bk1C/xlBkXCQBpzn1l0AAAAAgiM3pkPzfyRNplKGF/XSmQ==; nlbi_249257=ecthUKHeETDxVQjosHLyrwAAAADPx18T6TqNLrTvxH4REMyp; cookie-accepted=1; cookie-agreed=2; incap_ses_730_249257=N7kIAJpOtlLxAZGYO3whCpj81l0AAAAAYsFMaPMWyA+j7FQmB6PkKg==; incap_ses_729_249257=N3m4UbpzR02MPUjp0e4dCpj81l0AAAAAHHNqwNleaefrk2XUBay7EQ==; XSRF-TOKEN=aaeeaab6-8806-4969-a2aa-a614eb26839c; incap_ses_728_249257=0I5UT9eb6nYZf8SmOWEaCrYD110AAAAAVQPlGdmxFk08ciGSEKDupw==; incap_ses_534_249257=VsSmSahkT213UZfoWkBpB7cD110AAAAAbVHIdnvHnbDQYpsijQGxdg==; incap_ses_184_249257=rO2lWCZlM37pg6t5xbSNArcD110AAAAAszOA1TzbbtKID5nRYO9WdA==; incap_ses_408_249257=u2WBOQbYmWAOk64+toOpBcID110AAAAA4eyIEexbzPXnQH01soQE0Q==; incap_ses_876_249257=9zLGSUzhsG8skY+lUi4oDMED110AAAAASvmfK1SLKtI5Fy4NjS9R+g==; incap_ses_246_249257=DkGIRt2P73tGaTGF+vdpA8ID110AAAAAcVeCZpbuzVlWGxgdeCFj1Q==; incap_ses_877_249257=tQB6G5D5whqE34aU6LsrDMID110AAAAAgjj9FFWDOe7LkF4w2XtCVA==',
        }


        my_bar = st.progress(0)
        for counter, formation in enumerate(formations):
            with st.spinner('Loading data for the keyword '+ formation.upper()):
                all_form_city = {}
                for code in cities:
                    data1 = '{"quoi":"%s","ou":{"codePostal":"%s","type":"CP","modality":"0"},"nombreOccurences":10000,"debutPagination":1,"sort":"DISTANCE"}' % (formation, code)

                    response1 = requests.post(
                        'https://www.moncompteformation.gouv.fr/espace-prive/sl6-portail-web/public/formations',
                        headers=headers,
                        data=data1)

                    all_form_city[code] = response1.json()["item"]

                data2 = '{"quoi":"%s","ou":{"modality":"2"},"nombreOccurences":10000,"debutPagination":1,"sort":"SCORE"}' % formation

                response2 = requests.post(
                    'https://www.moncompteformation.gouv.fr/espace-prive/sl6-portail-web/public/formations',
                    headers=headers,
                    data=data2)

                all_form_city['distance'] = response2.json()["item"]

                df = pd.DataFrame()
                for dict_city in all_form_city.values():
                    if len(dict_city)!=0:
                        df_city = pd.DataFrame.from_dict(dict_city)
                        df_city = pd.concat([df_city.drop(['id'], axis=1), df_city['id'].apply(pd.Series)], axis=1)
                        df = pd.concat([df, df_city])

                if len(df)!=0:
                    df = df.drop_duplicates(subset=['title', 'organism', 'codePostal', 'ville', 'duration', 'prixTotalTTC',"numeroFormation","numeroAction"])
                    frames[formation] = df
                    formations_new.append(formation)


            my_bar.progress((counter + 1)/len(formations))
    st.success('Data loaded !')
    return frames, formations_new

@st.cache
def aggregate_df(frames):
    with st.spinner('Please wait : the app is aggregating data'):
        df = pd.DataFrame()
        frames_copy = copy.deepcopy(frames)
        for formation, details in frames_copy.items():
            details['Keyword'] = formation
        for df_form in frames_copy.values():
            df = pd.concat([df, df_form])
        df = df.drop_duplicates(subset=['title', 'organism', 'codePostal', 'ville', 'duration', 'prixTotalTTC',"numeroFormation","numeroAction"])
        df = df[['title', 'organism', 'codePostal', 'ville','distance', 'duration', 'prixTotalTTC','Keyword']]
    return df

def check_distance_or_not(str):
    if str == 'A DISTANCE':
        return 'Distance'
    else:
        return 'Présentiel'

@st.cache
def get_communes():
    communes = pd.DataFrame()
    code_dept = []
    dept = []

    with urlopen('https://raw.githubusercontent.com/gregoiredavid/france-geojson/master/departements.geojson') as response:
        counties = json.load(response)

    for feat in counties['features']:
        feat['id']=feat['properties']['code']
        code_dept.append(feat['properties']['code'])
        dept.append(feat['properties']['nom'])

    communes['Code Dept']=code_dept
    communes['Département']=dept

    return counties, communes

@st.cache
def clean_data(df):
    with st.spinner('Please wait : the app is cleaning data'):
        df_copy = df.copy()
        df_copy[['Ville', 'Code Postal']] = df_copy[[
            'ville', 'codePostal']].fillna(value='A DISTANCE')
        df_copy['Durée'] = df_copy['duration'].replace(
            {0: df_copy['duration'].mean()})
        df_copy['Durée'] = df_copy['Durée'].fillna(df_copy['Durée'].mean())
        df_copy['Ville'] = df_copy['Ville'].str.upper()
        df_copy['Ville'] = df_copy['Ville'].str.normalize('NFKD').str.encode('ascii', errors='ignore').str.decode('utf-8')
        df_copy["Ville"] = df_copy["Ville"].str.replace('CEDEX', '')
        df_copy["Ville"] = df_copy["Ville"].str.replace('-', ' ')
        df_copy["Ville"] = df_copy["Ville"].str.replace("'", ' ')
        df_copy["Ville"] = df_copy["Ville"].str.replace('[0-9]', '')
        df_copy["Ville"] = df_copy["Ville"].str.replace('PARIS LA DEFENSE', 'PUTEAUX')
        df_copy["Ville"] = df_copy["Ville"].str.replace('PARIS.*', 'PARIS')
        df_copy["Ville"] = df_copy["Ville"].str.replace('LYON.*', 'LYON')
        df_copy["Ville"] = df_copy["Ville"].str.replace('MARSEILLE.*', 'MARSEILLE')
        df_copy['Ville'] = df_copy['Ville'].str.replace(' ST ',' SAINT ')
        df_copy['Ville'] = df_copy['Ville'].str.replace(' STE ',' SAINTE ')
        df_copy['Ville'] = df_copy['Ville'].str.replace('ST ','SAINT ')
        df_copy['Ville'] = df_copy['Ville'].str.replace('STE ','SAINTE ')
        df_copy['Ville'] = df_copy['Ville'].str.replace('FUTUROSCOPE','POITIERS')
        df_copy['Ville'] = df_copy['Ville'].str.replace('ERAGNY SUR OISE','ERAGNY')
        df_copy['Ville'] = df_copy['Ville'].str.replace('SOPHIA ANTIPOLIS','NICE')
        df_copy['Ville'] = df_copy['Ville'].str.replace('VERRIERES EN ANJOU','ANGERS')
        df_copy['Ville'] = df_copy['Ville'].str.replace('CHERBOURG EN COTENTIN','CHERBOURG OCTEVILLE')
        df_copy['Ville'] = df_copy['Ville'].str.replace('FRANCONVILLE LA GARENNE','FRANCONVILLE')
        df_copy['Ville'] = df_copy['Ville'].str.replace('BEAUPREAU EN MANGES','BEAUPREAU')
        df_copy['Ville'] = df_copy['Ville'].str.replace('ROMAGNY FONTENAY','ROMAGNY')
        df_copy['Ville'] = df_copy['Ville'].str.replace('SAINT JUSAINT SAINT RAMBERT','SAINT JUST SAINT RAMBERT')
        df_copy['Ville'] = df_copy['Ville'].str.replace('SAINT PRIESAINT EN JAREZ','SAINT PRIEST EN JAREZ')
        df_copy['Ville'] = df_copy['Ville'].str.replace('BAGNOLES DE L ORNE NORMAND','BAGNOLES DE L ORNE')
        df_copy['Ville'] = df_copy['Ville'].str.replace('LES ACHARDS','ACHARDS')
        df_copy['Ville'] = df_copy['Ville'].str.replace('ORLY AEROGARE','ORLY')
        df_copy["Ville"] = df_copy["Ville"].str.strip()

        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('69465', '69006')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('49480', '49000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33701', '33700')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35407', '35400')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33401', '33400')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('34197', '34000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33405', '33400')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33008', '33000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('85016', '85000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('95092', '95000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('29330', '29000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35605', '35600')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^1100$', '01100')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('06900', '06000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('06001', '06000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33504', '33500')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('44105', '44100')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('86012', '86000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('62401', '62400')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('53062', '53000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('97421', '97420')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35571', '35135')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('50130', '50100')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('11890', '11000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35306', '35300')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('01002', '01000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^3630$', '03630')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('34521', '34500')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('94390', '94310')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('06900', '06000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('85150', '85152')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('34935', '34000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('80046', '80000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('80083', '80000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('80090', '80000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('62012', '62000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('62027', '62000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('59328', '59300')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('95891', '95000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('38025', '38000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('66004', '66000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('50460', '50100')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('21065', '21000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35577', '35510')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33074', '33000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33076', '33000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('62228', '62100')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('17024', '17000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92060', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('31023', '31000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('81012', '81000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('37206', '37200')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('54064', '54000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('28008', '28000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('86010', '86000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92088', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('29285', '29200')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^8500$', '08500')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('44603', '44600')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('31074', '31000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('20090', '20000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('59703', '59700')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35704', '35700')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('79027', '79000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('94573', '94150')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('12033', '12000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('59312', '59300')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('38025', '38000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92908', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^8500$', '08500')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35704', '35700')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('13591', '13080')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^6400$', '06400')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^2100$', '02100')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35042', '35000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('45006', '45000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92910', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('44275', '44200')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33060', '33000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('80080', '80000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92916', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('91192', '91190')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('06902', '06000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('17183', '17180')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^6560$', '06560')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('17183', '17180')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('86960', '86000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('806300', '86300')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('59042', '59000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('31077', '31000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92053', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('006200', '06200')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^6000$', '06000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('33071', '33000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('80003', '80000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('27091', '27000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^6600$', '06600')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('29679', '29600')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^8210$', '08210')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('22005', '22000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('206300', '26300')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('063000', '63000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('062000', '62000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('36028', '36000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('44822', '44800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('69456', '69006')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92062', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92044', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('92196', '92800')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('69443', '69004')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('31675', '31670')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('84140', '84000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('97490', '97400')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^6200$', '06200')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('06299', '06200')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('75116', '75016')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('06088', '06000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('69351', '69003')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('64075', '64000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35172', '35170')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('42007', '42000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('35207', '35200')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('87069', '87000')
        df_copy["Code Postal"] = df_copy["Code Postal"].str.replace('^6300$', '06300')


        df_copy['Organisme'] = df_copy['organism'].str.upper()
        df_copy['Tarif horaire'] = df_copy['prixTotalTTC'] / df_copy['Durée']
        df_copy['Tarif horaire'] = df_copy['Tarif horaire'].fillna(
            df_copy['Tarif horaire'].mean())
        df_copy['Présentiel ou à distance'] = df_copy['Ville'].apply(
            check_distance_or_not)
        df_copy = df_copy.rename(
            columns={
                'title': 'Nom',
                'prixTotalTTC': 'Tarif TTC'})
        df_copy = df_copy[['Nom',
                           'Organisme',
                           'Ville',
                           'Code Postal',
                           'Durée',
                           'Tarif TTC',
                           'Tarif horaire',
                           'Présentiel ou à distance',
                           'Keyword']]
        df_copy = df_copy.sort_values(by='Ville')
    return df_copy

def filter(new_df, cities, organism, form, hour_min, distance):
    mode = 'perso'
    filtered_df = new_df.copy()
    filtered_df = filtered_df[filtered_df['Durée'] > hour_min]
    if len(cities) != 0 :
        filtered_df = filtered_df[(filtered_df['Ville'].isin(cities))]
        mode ='city'
    if len(organism) != 0:
        filtered_df = filtered_df[(filtered_df['Organisme'].isin(organism))]
    if len(form) != 0:
        filtered_df = filtered_df[filtered_df['Keyword'].isin(form)]
    if distance:
        filtered_df = filtered_df[filtered_df['Ville'] != 'A DISTANCE']
    return mode, filtered_df

def show(new_df, mode, graph, details,distance):
    with st.spinner('Please wait : the app is preparing data for visualization'):
        st.write('')
        '''
        **Nombre de formations :**
        '''
        st.write(len(new_df))

        '''
        **Tarif horaire moyen des formations :**
        '''
        st.write(np.round(new_df['Tarif horaire'].mean(), 2),'€')

        '''
        **Durée moyenne des formations :**
        '''
        st.write(np.round(new_df['Durée'].mean(), 2), 'heures')

        '''
        **Tarif moyen des formations :**
        '''
        st.write(np.round(new_df['Tarif TTC'].mean(), 2),'€')

        if mode=='global':
            '''
            **Tarif horaire moyen des formations longues (ie > 140 heures) :**
            '''
            st.write(np.round(new_df[new_df['Durée']>140]['Tarif horaire'].mean(), 2),'€')

            '''
            **Tarif horaire moyen des formations courtes (ie < 140 heures):**
            '''
            st.write(np.round(new_df[new_df['Durée']<140]['Tarif horaire'].mean(), 2),'€')

        '''
        **TOP 50 des organismes proposant le plus de formations  :**
        '''
        organism = pd.DataFrame(
            new_df.groupby(
                by='Organisme').count()['Nom'].values,
            index=new_df.groupby(
                    by='Organisme').count()['Nom'].index,
            columns=['Nombre'])
        organisme_50 = organism.sort_values(by='Nombre', ascending=False)[:50]
        fig = px.bar(x=organisme_50.index, y=organisme_50['Nombre'].values)
        st.plotly_chart(fig)

        if mode!='city' and distance==False:
            '''
            **Répartition présentiel / à distance  :**
            '''
            values = [new_df['Présentiel ou à distance'][new_df['Présentiel ou à distance'] == 'Présentiel'].count(
            ), new_df['Présentiel ou à distance'][new_df['Présentiel ou à distance'] == 'Distance'].count()]
            fig = go.Figure(
                data=[
                    go.Pie(
                        labels=[
                            'Présentiel',
                            'A distance'],
                        values=values,
                        hole=.3)])
            st.plotly_chart(fig)

        '''
        **Résumé statistique :**
        '''
        st.write(new_df.describe())

        if graph:
            '''
            **Tarif horaire selon la durée des formations  :**
            '''
            fig = px.scatter(
                new_df,
                x='Tarif horaire',
                y='Durée',
                color='Ville',
                hover_name='Organisme',
                marginal_y="histogram",
                marginal_x="histogram",
                range_x=[0,200])
            st.plotly_chart(fig)

            '''
            **Distribution des tarifs horaires  :**
            '''
            fig = px.histogram(
                new_df,
                x="Tarif horaire",
                color='Ville',
                hover_data=new_df.columns,
                range_x=[0,200])
            st.plotly_chart(fig)

        if details:
            '''
            **Détails des formations:**
            '''
            st.dataframe(new_df)

def carto_clean(new_df,counties, communes) :
    px.set_mapbox_access_token(open(".mapbox_token").read())

    postal_code = pd.read_csv('population.csv')
    postal_code['Code Postal'] = postal_code['Code Postal'].astype('str')
    postal_code['Code Postal'] = postal_code['Code Postal'].str.replace('R','0')
    postal_code['Code Département'] = postal_code['Code Département'].astype('str')
    postal_code['Code Département'] = postal_code['Code Département'].str.replace('R','0')

    form_presence = new_df[new_df['Code Postal']!='A DISTANCE']
    form_presence['Code Postal'] = form_presence['Code Postal'].astype('str')
    form_presence_by_city = form_presence.groupby(["Ville","Code Postal"]).count()
    form_presence_by_city = form_presence_by_city['Nom']
    form_presence_by_city.name = 'Nombre de formations'
    form_presence_by_city=form_presence_by_city.reset_index()

    form_by_city = pd.merge(postal_code,form_presence_by_city,left_on=['Commune','Code Postal'],right_on=["Ville","Code Postal"])
    #st.write(form_presence_by_city[['Ville','Code Postal','Nombre de formations']][form_presence_by_city['Code Postal'].isin(form_by_city['Code Postal'])==False])
    #st.write(form_presence_by_city[['Nombre de formations']][form_presence_by_city['Code Postal'].isin(form_by_city['Code Postal'])==False].sum())

    form_by_city = form_by_city.dropna()

    form_by_dep = form_by_city.groupby('Code Département').sum().reset_index()
    form_by_dep = pd.merge(form_by_dep,communes,left_on='Code Département',right_on='Code Dept')

    return form_by_dep, form_by_city

@st.cache
def show_graph_by_city(form_by_city):

    new_form_by_city = form_by_city.copy()

    new_form_by_city['Nombre de formations']=pd.to_numeric(new_form_by_city['Nombre de formations'], errors='coerce')

    form_big_city = new_form_by_city.groupby(['Commune','Code Département']).agg({'Population':'sum','latitude':'median','longitude':'median','Nombre de formations':'sum'}).reset_index()
    form_big_city = form_big_city[form_big_city['Population']>10000]
    form_big_city['Formations / 1000 Habitants']=form_big_city['Nombre de formations']/form_big_city["Population"]*1000


    return form_big_city

@st.cache
def show_graph_by_dep(form_by_dep):
    new_form_by_dep=form_by_dep.copy()
    new_form_by_dep['Nombre de formations']=pd.to_numeric(new_form_by_dep['Nombre de formations'], errors='coerce')
    new_form_by_dep["Population"]=pd.to_numeric(new_form_by_dep["Population"], errors='coerce')

    new_form_by_dep['Formations / 1000 Habitants']=new_form_by_dep['Nombre de formations']/new_form_by_dep["Population"]*1000

    return new_form_by_dep

#########################################################################
###############################    Main    ##############################
#########################################################################

reload = st.sidebar.button("Cliquer pour MAJ les données")

if reload:
    frames_formations, formations_new = load_data(formations)
    df = aggregate_df(frames_formations)
    df = clean_data(df)
    df.to_csv("formations_extract.csv", index=False)
else:
    df = pd.read_csv("formations_extract.csv")

navigation = st.sidebar.radio("Navigation",('Home','Résumé', 'Vue analytique','Vue cartographique'))

if navigation=='Home':
    st.write('------------------------')
    st.write("Vision analytique des formations proposées sur le site web et l'app mobile Mon Compte Formation.")
    st.write("*Vous pouvez mettre à jour les données en cliquant sur le bouton dans la barre latérale. Attention : le chargement met une vingtaine de minutes.*")
    st.write("Les données affichées correspondent à l'intégralité des formations proposées sur l'app Mon Compte Formation pour les mot-clés suivants : ")
    st.write(formations)
    st.write("Source des données : https://www.moncompteformation.gouv.fr/")

elif navigation=='Résumé':
    new_df = df.copy()
    distance = st.sidebar.checkbox('Ne pas inclure les formations à distance')
    details = st.sidebar.checkbox('Afficher le détails de toutes les formations')
    graph = st.sidebar.checkbox('Afficher les graphiques des tarifs horaires')

    st.write('------------------------')
    st.write("Les données affichées ci-dessous correspondent à l'intégralité des formations proposées sur l'app Mon Compte Formation pour les mot-clés listés (voir onglet Home pour la liste des mots-clés)")

    show(new_df, 'global', graph, details,distance)


elif navigation=='Vue analytique':
    new_df = df.copy()
    st.write('------------------------')
    st.write("Les données affichées ci-dessous correspondent aux formations proposées sur l'app Mon Compte Formation qui satisfont aux filtres demandés, pour les mot-clés choisis (voir onglet Home pour la liste des mots-clés)")
    form = st.sidebar.multiselect('Types de formations', new_df['Keyword'].unique())
    cities = st.sidebar.multiselect('Villes', new_df['Ville'].unique())
    organism = st.sidebar.multiselect('Organismes de formation', new_df['Organisme'].unique())
    hour_min = st.sidebar.slider('Durée minimum de la formation (en heures)', math.floor( new_df['Durée'].min()), math.ceil(new_df['Durée'].max()), math.floor( new_df['Durée'].min()))
    distance = st.sidebar.checkbox('Ne pas inclure les formations à distance')
    details = st.sidebar.checkbox('Afficher le détails de toutes les formations')
    graph = st.sidebar.checkbox('Afficher les graphiques des tarifs horaires')

    # Filter the dataframe
    mode, filtered_df = filter(new_df, cities, organism, form, hour_min, distance)

    show(filtered_df, mode, graph, details,distance)

elif navigation=='Vue cartographique':
    new_df = df.copy()

    gran = st.sidebar.radio('Granularité', ('Par Département', 'Par Ville'))
    form = st.sidebar.multiselect('Types de formations', new_df['Keyword'].unique())
    organism = st.sidebar.multiselect('Organismes de formation', new_df['Organisme'].unique())

    hour_min = st.sidebar.slider('Durée minimum de la formation (en heures)', math.floor( new_df['Durée'].min()), math.ceil(new_df['Durée'].max()), math.floor( new_df['Durée'].min()))

    counties, communes = get_communes()

    mode, filtered_df = filter(new_df, [], organism, form, hour_min, True)

    form_by_dep, form_by_city = carto_clean(filtered_df, counties, communes)
    st.write('------------------------')

    if gran=='Par Département':
        new_form_by_dep = show_graph_by_dep(form_by_dep)

        st.write("Les données affichées ci-dessous correspondent à l'intégralité des formations proposées sur l'app Mon Compte Formation pour les mot-clés listés (voir onglet Home pour la liste des mots-clés)")

        '''
        **Nombre de formations**
        '''
        fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=new_form_by_dep['Code Dept'], z=new_form_by_dep['Nombre de formations'],colorscale="YlGnBu",hovertext=new_form_by_dep['Département']));
        fig.update_layout(mapbox_style="carto-positron",
                          mapbox_zoom=4.5, mapbox_center = {"lat": 46.7, "lon": 1.7});
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0});
        st.plotly_chart(fig)

        '''
        **Nombre de formations pour 1000 Habitants**
        '''
        fig = go.Figure(go.Choroplethmapbox(geojson=counties, locations=new_form_by_dep['Code Dept'], z=new_form_by_dep['Formations / 1000 Habitants'],colorscale="YlGnBu",hovertext=new_form_by_dep['Département']));
        fig.update_layout(mapbox_style="carto-positron",
                          mapbox_zoom=4.5, mapbox_center = {"lat": 46.7, "lon": 1.7});
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0});
        st.plotly_chart(fig)


    elif gran=='Par Ville':

        form_big_city = show_graph_by_city(form_by_city)

        st.write("Les données affichées ci-dessous correspondent aux formations proposées dans les **villes de plus de 10.000 habitants** sur l'app Mon Compte Formation pour les mot-clés listés (voir onglet Home pour la liste des mots-clés)")

        '''
        **Nombre de formations**
        '''
        fig = px.scatter_mapbox(form_big_city, lat="latitude", lon="longitude", size="Nombre de formations",
                          color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=3.7, hover_name='Commune')
        st.plotly_chart(fig)

        '''
        **Nombre de formations pour 1000 habitants**
        '''
        fig = px.scatter_mapbox(form_big_city, lat="latitude", lon="longitude", size="Formations / 1000 Habitants",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=3.7, hover_name='Commune')
        st.plotly_chart(fig)

        '''
        **Top des villes de plus de 30.000 habitants où le nombre de formations pour 1000 habitants est le plus faible**
        '''
        form_city_targeted = form_big_city[(form_big_city['Population']>30000) ]
        form_city_targeted['Inverse de Formations / 1000 Habitants'] = 1/form_city_targeted['Formations / 1000 Habitants']
        fig = px.scatter_mapbox(form_city_targeted.sort_values(by='Formations / 1000 Habitants'),lat="latitude", lon="longitude", size="Inverse de Formations / 1000 Habitants",
                  color_continuous_scale=px.colors.cyclical.IceFire, size_max=15, zoom=3.7, hover_name='Commune')
        st.plotly_chart(fig)
