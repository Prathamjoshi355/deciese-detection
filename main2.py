from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import numpy as np
from io import BytesIO
from PIL import Image
import tensorflow as tf

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

MODEL = tf.keras.models.load_model("IMAGE.h5")
CLASS_NAMES = ["ANIMAL", "CROP"]
MODEL1 = tf.keras.models.load_model("ANIMAL.keras")
CLASS_NAMES1 = ["Lumpy skin", "Healthy"]
MODEL2 = tf.keras.models.load_model("CROP.keras")
CLASS_NAMES2 = ["Early_blight", "Late_blight", "GOOD"]

@app.get("/ping")


async def ping():
    return "Hello, I am alive"


def read_file_as_image(data) -> np.ndarray:
    image = np.array(Image.open(BytesIO(data)))
    return image


@app.post("/predict")
async def predict(
        file: UploadFile = File(...)
):
    image = read_file_as_image(await file.read())
    img_batch = np.expand_dims(image, 0)

    predictions = MODEL.predict(img_batch)

    image1 = CLASS_NAMES[np.argmax(predictions[0])]
    confidence = np.max(predictions[0])

    c="ANIMAL"
    c1="CROP"


    if image1 == c:
        predictions = MODEL1.predict(img_batch)
        predicted_class=CLASS_NAMES1[np.argmax(predictions[0])]
        confidence = np.max(predictions[0])
    elif image1 == c1:
        predictions = MODEL2.predict(img_batch)
        predicted_class=CLASS_NAMES2[np.argmax(predictions[0])]
    else:
        print('r')

    return {

        'GIVEN OBJECT':image1,
        'CLASS': predicted_class,
        'CONFIDENCE': float(confidence * 100)
    }


if __name__ == "__main__":
    uvicorn.run(app, host='localhost', port=8000)