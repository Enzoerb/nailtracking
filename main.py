import tkinter as tk
from interface.main import WebcamApp
from src.main import nailTracking
import tensorflow.compat.v1 as tf

args = {
    "model": "./src/model/nail_inference_graph.pb",
    "min_confidence": 0.5
}

if __name__ == "__main__":
    model = tf.Graph()

    with model.as_default():
        print("> ====== loading NAIL frozen graph into memory")
        graphDef = tf.GraphDef()

        with tf.gfile.GFile(args["model"], "rb") as f:
            serializedGraph = f.read()
            graphDef.ParseFromString(serializedGraph)
            tf.import_graph_def(graphDef, name="")
        print(">  ====== NAIL Inference graph loaded.")

        root = tk.Tk()
        app = WebcamApp(root, "Power Nail by Pixel Power - v1.0.0", nailTracking, model)
