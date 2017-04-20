from learning.retina_net import RetiNet
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, confusion_matrix
from keras.utils.np_utils import to_categorical
import h5py
import numpy as np


def main(model_conf, train_data, test_data):

    # Load model and set last layer
    print "Loading model..."
    net = RetiNet(model_conf)
    net.set_intermediate('flatten_3')

    # Get CNN codes
    print "Getting features..."
    train_codes = net.predict(train_data)

    # Create random forest
    rf = RandomForestClassifier()
    X_train = train_codes['probabilities']
    y_train = train_codes['y_true']

    print "Training RF..."
    rf.fit(X_train, y_train)

    # Load test data
    test_codes = net.predict(test_data)
    X_test = test_codes['probabilities']
    y_true = test_codes['y_true']

    # Predict
    print "Getting predictions..."
    y_pred = rf.predict(X_test)

    print accuracy_score(y_true, y_pred)
    print confusion_matrix(y_true, y_pred)
    print classification_report(y_true, y_pred)


if __name__ == '__main__':

    import sys

    main(sys.argv[1], sys.argv[2], sys.argv[3])