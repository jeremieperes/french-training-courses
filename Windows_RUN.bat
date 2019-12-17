cd %~dp0
git clone https://github.com/jeremieperes/french-training-courses.git
cd french-training-courses
pip install -r requirements.txt
cd app
streamlit run Formation-web-app.py
