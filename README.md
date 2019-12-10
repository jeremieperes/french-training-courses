# Web app "Mon Compte Formation"

Web app providing a statistical analysis of French digital training courses offered on the website / mobile app "Mon Compte Formation", launched in November 2019 by the French Governement.

Data source : https://www.moncompteformation.gouv.fr/

## How’s it work?

1. Clone GitHub repo
```
git clone https://github.com/jeremieperes/french-training-courses
```
2. Install required python packages :
```
cd path/to/project/directory
pip install -r requirements.txt
```
3. Run the streamlit command line
```
streamlit run app/Formation-web-app.py
```

*Note : it may take up to 15 minutes to load data for the first time*

## Screenshots

* **KPIs**

![Vue Résumé](images/Resume.png)
![Vue analytique](images/Vue-analytique.png)

* **Filtered View**

![Vue analytique filtrée](images/Vue-filtre.png)

* **Cartographic View**

![Vue cartographique par département](images/Vue-carto-departement.png)
![Vue cartographique par ville](images/Vue-carto-ville.png)
