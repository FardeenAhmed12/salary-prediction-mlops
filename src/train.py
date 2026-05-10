import pickle
from data_preprocessing import load_data
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import numpy as np

DATA_PATH = 'data/salary_data.csv'
MODEL_PATH = 'models/model.pkl'

def train():
    X: np.ndarray
    y: np.ndarray
    X, y = load_data(DATA_PATH)
    X_train: np.ndarray
    X_test: np.ndarray
    y_train: np.ndarray
    y_test: np.ndarray
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    model = LinearRegression()
    model.fit(X_train, y_train)
    
    predictions: np.ndarray = model.predict(X_test)
    mse = mean_squared_error(y_test, predictions)
    mae = mean_absolute_error(y_test, predictions)
    r2 = r2_score(y_test, predictions)
    
    print(f'MSE: {mse}, MAE: {mae}, R2: {r2}')
    
    with open(MODEL_PATH, 'wb') as f:
        pickle.dump(model, f)

if __name__ == '__main__':
    train()