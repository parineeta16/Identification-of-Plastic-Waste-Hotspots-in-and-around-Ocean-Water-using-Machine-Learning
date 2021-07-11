from flask import Flask, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from util import base64_to_pil
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()
import json

with open('config.json','r') as c:
    params = json.load(c)["params"]

local_server = "True"

app = Flask(__name__)
if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["local_uri"]
else:
    app.config['SQLALCHEMY_DATABASE_URI'] = params["prod_uri"]
db = SQLAlchemy(app)


class Contact(db.Model):
    S_No = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(80), unique=False, nullable=False)
    Date = db.Column(db.String(12), unique=False, nullable=True)
    Email = db.Column(db.String(35), unique=False, nullable=False)
    Phone = db.Column(db.String(12), unique=False, nullable=False)
    Message = db.Column(db.String(120), unique=False, nullable=False)


@app.route("/")
def home():
    return render_template('index.html')


@app.route("/contact", methods=['Get', 'Post'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        message = request.form.get('msg')
        entry = Contact(Name=name, Phone=phone, Message=message, Date=datetime.now(), Email=email)
        db.session.add(entry)
        db.session.commit()

    return render_template('contact.html')


@app.route("/mission")
def mission():
    return render_template('mission.html')


@app.route("/team")
def team():
    return render_template('team.html')


@app.route("/object")
def object():
    return render_template('hotspot1.html')


@app.route("/hotspot")
def hotspot():
    return render_template('hotspot.html')

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method == 'POST':
        # Get the image from post request
        img = base64_to_pil(request.json)
        # Save the image to ./uploads
        img.save("/var/www/FlaskApp/FlaskApp/tf_files/image.png")
        img = img.resize((224, 224))
        print("image saved")
        # Make prediction
        #preds = model_predict(img)

        # Preprocessing the image
        #x = image.img_to_array(img)
        # x = np.true_divide(x, 255)
        #x = np.expand_dims(x, axis=0)

        # Be careful how your trained model deals with the input
        # otherwise, it won't make correct prediction!
        #x = preprocess_input(x, mode='tf')

        #preds = model.predict(x)
        #!!!!!!!!!!!!!!!!
        image_data = tf.io.gfile.GFile("/var/www/FlaskApp/FlaskApp/tf_files/image.png", 'rb').read()
        print("Image read")
        label_lines = [line.rstrip() for line
                           in tf.io.gfile.GFile("/var/www/FlaskApp/FlaskApp/tf_files/retrained_labels.txt")]

        print("Implementing model")

        # Unpersists graph from file
        with tf.io.gfile.GFile("/var/www/FlaskApp/FlaskApp/tf_files/retrained_graph.pb", 'rb') as f:
            graph_def = tf.compat.v1.GraphDef()
            graph_def.ParseFromString(f.read())
            _ = tf.import_graph_def(graph_def, name='')

        print("Model")

        with tf.compat.v1.Session() as sess:
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
            
            predictions = sess.run(softmax_tensor,
                     {'DecodeJpeg/contents:0': image_data})

            print("Making Predictions")
            
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            
            for node_id in top_k:
                human_string = label_lines[node_id]
                score = predictions[0][node_id]
                if human_string == 'plastic':
                    #print(str(score))
                    score = score*100
                    score = "{:.2f}".format(score)
                    result ="Plastic-" + str(score)
                    #print('%s (score = %.2f)' % (human_string, score))
        # Process your result for human
        #pred_proba = "{:.3f}".format(np.amax(preds))    # Max probability
        #pred_class = decode_predictions(preds, top=1)   # ImageNet Decode

        #result = str(pred_class[0][0][1])               # Convert to string
        #result = result.replace('_', ' ').capitalize()
        #score = str(score)
        #result ="Plastic-" + str(score)
        print(result,"as")
        # Serialize the result, you can add additional fields
        return jsonify(result=result)

    return None

app.run(host = '0.0.0.0', port = 5000, debug=True)  # Debug= True will give you latest output without running code again and again
