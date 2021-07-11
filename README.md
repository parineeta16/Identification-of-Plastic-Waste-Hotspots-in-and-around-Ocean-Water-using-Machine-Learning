# Local Installation

##### 1. First, clone the repo
$ git clone https://github.com/parineeta16/Identification-of-Plastic-Waste-Hotspots-in-and-around-Ocean-Water-using-Machine-Learning.git
$ cd Identification-of-Plastic-Waste-Hotspots-in-and-around-Ocean-Water-using-Machine-Learning-master

##### 2. Install Python packages
$ pip install -r requirements.txt

##### 3. Run!
$ python main.py

Open http://localhost:5000 

1. Users can upload images using upload button or drag option to predict plastic accuracy.
2. Click on predict button after uploading the image to get the result.
3. Under Plastic Hotspot Detection, find the tableau workbooks with plastic location visualization.

# Hosting the Website

##### 1. Take remote access of your instance.

##### 2. Install Apache2, phpMyAdmin, MySQL, Python, and Python packages (Numpy, Pandas, PIL), TensorFlow in your instance.

##### 3. Import your local database into the database of the instance using the "stop marine pollution.sql" file.

##### 4. Create a folder named "FlaskApp" in /var/www/ and clone your git repository into the FlaskApp folder using 
$ git clone your_repository_from_github

##### 5. Go into the FlaskApp folder and run the main file.
$ cd /var/www/FlaskApp  \
$ python3 main.py

##### 6. Open http://ip:5000


