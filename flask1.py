from flask import Flask, render_template, request, url_for
import pytesseract
from PIL import Image
import os
from gtts import gTTS
#from googletrans import Translator
from google_trans_new import google_translator

app = Flask(__name__)

app.config["IMAGE_UPLOADS"] = os.path.join(app.root_path, 'static/img/uploads')

def getAudioUrl(filename):
    return "audio-"+filename.split(".")[0]+".mp3"


@app.route("/home")
@app.route("/", methods=["GET", "POST"])
def upload_image():
    filename = ""
    if request.method == "POST":

        if request.files:
            l = request.form['select']
            print(l)
            if l == "Kannada":
                language = 'kan'
            elif l == "English":
                language = 'eng'
            elif l == "Hindi":
                language = 'hin'
            elif l == "Sanskrit":
                language = 'san'

            image = request.files["image"]
            image.save(os.path.join(app.root_path, 'static/img/uploads', image.filename))
            print("IMAGE SAVED")
            filename = image.filename
            print(image.filename)

            # image_url = r"D:\Flask\static\img\uploads\\" + image.filename
            image_url = os.path.join(app.root_path, 'static/img/uploads', image.filename)
            image = Image.open(image_url)
            # pytesseract.pytesseract.tesseract_cmd = os.path.join(app.root_path, 'TesseractOCR/tesseract.exe')
            try:
                imageText = pytesseract.image_to_string(image, lang=language)
                print()
                translator = google_translator() 
                translatedText = translator.translate(imageText)
                print(translatedText)
            except:
                imageText ="No Text Found"
                translatedText = "No Text Found"
        print("Text Ready!")

        if l == "Kannada":
            language = 'kn'
        elif l == "English":
            language = 'en'
        elif l == "Hindi":
            language = 'hi'
        elif l == "Sanskrit":
            language = 'sk'

        myObj = gTTS(text=imageText, lang=language, slow=False)
        audioFile = getAudioUrl(filename)
        myObj.save("static/audio/"+audioFile)
        data = imageText
        key = translatedText

        return render_template("upload_image.html", data=data, key=key, audioFile = audioFile)

    else:
        return render_template("upload_image.html")


if __name__ == "__main__":
    app.run(debug=True)
