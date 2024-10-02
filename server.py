from flask import Flask, request, send_from_directory, send_file
from fastai.vision.all import *
import zipfile 
import os
import pathlib

app = Flask(__name__, static_folder='static')

@app.route("/")
def hello_world():
    return send_from_directory("static", "index.html") 

@app.route("/images", methods=["POST"])
def images():
    file = request.files["images"]
    # check compression method zip/tar/gzip

    file.save("./test.zip")

    dataPath = os.getcwd() + "/test"
    
    # decompress zip
    with zipfile.ZipFile("./test.zip", mode="r") as f:
        f.extractall("./test")

    images = get_image_files(dataPath)

    print(f'Images found: %i', len(images))

    failed = verify_images(images)

    # remove corrupted images
    print(f'Images corrupted: %i', len(failed))
    failed.map(Path.unlink)

    model = DataBlock(
            blocks=(ImageBlock, CategoryBlock),
            get_items=get_image_files,
            splitter=RandomSplitter(valid_pct=0.2, seed=42),
            get_y=parent_label,
            item_tfms=Resize(128)
            )

    dls = model.dataloaders(dataPath)  
    learn = vision_learner(dls, resnet18, metrics=error_rate)
    learn.fine_tune(4)

    export = learn.export()

    return "ok"

@app.route("/test")
def test():
    return "ok"

@app.route("/download")
def download():
    try:
        return send_file(pathlib.Path().resolve() / "export.pkl", as_attachment=True)
    except Exception as e:
        return str(e)

@app.route("/upload")
def upload():
    model = request.file[0]

    # save model

    learn_inf = load_learner(path/'export.pkl')
    return "ok"

