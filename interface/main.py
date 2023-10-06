from params import *
from utils import *

def analysis() -> np.ndarray:
    """
    Make a prediction using the latest trained model
    """

    print("\n⭐️ Use case: predict")

    # connect it to front end and API
    X_pred = api_request_pred(COORDS)

    model = load_model()
    assert model is not None

    X_processed = preprocess_features_pred(X_pred)
    X_processed = tf.expand_dims(X_processed, axis=0)
    print(X_processed.shape)

    y_pred = model.predict(X_processed)

    print("\n✅ prediction done: ", y_pred, y_pred.shape, "\n")
