"""
Flight Delay Prediction System using ML algorithms
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
from sklearn.metrics import confusion_matrix, classification_report, accuracy_score
import warnings
warnings.filterwarnings('ignore')

def generate_flight_data():
    """Generate synthetic flight delay dataset"""
    np.random.seed(42)
    n_samples = 2000
    
    data = {
        'Flight_Number': np.arange(1, n_samples + 1),
        'Departure_Hour': np.random.randint(0, 24, n_samples),
        'Temperature': np.random.normal(15, 10, n_samples),
        'Humidity': np.random.uniform(30, 100, n_samples),
        'Wind_Speed': np.random.exponential(5, n_samples),
        'Visibility': np.random.uniform(1, 10, n_samples),
        'Precipitation': np.random.exponential(2, n_samples),
        'Airport_Congestion': np.random.uniform(0, 100, n_samples),
        'Route_Distance': np.random.uniform(100, 5000, n_samples),
        'Historical_Delay': np.random.exponential(10, n_samples),
        'Aircraft_Age': np.random.uniform(1, 25, n_samples),
        'Airline_Performance': np.random.uniform(70, 99, n_samples),
    }
    
    df = pd.DataFrame(data)
    
    # Create target variable (delay in minutes)
    df['Delay_Minutes'] = (
        0.5 * df['Temperature'] + 
        0.3 * df['Wind_Speed'] + 
        0.2 * df['Precipitation'] +
        0.4 * df['Airport_Congestion'] +
        0.1 * df['Historical_Delay'] -
        0.3 * df['Airline_Performance'] +
        np.random.normal(0, 5, n_samples)
    )
    df['Delay_Minutes'] = df['Delay_Minutes'].clip(lower=0)
    
    # Create binary target (delayed or not)
    df['Is_Delayed'] = (df['Delay_Minutes'] > 15).astype(int)
    
    return df

def train_models(X_train, X_test, y_train, y_test):
    """Train multiple regression models"""
    models = {}
    results = {}
    
    # Linear Regression
    lr_model = LinearRegression()
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)
    results['Linear Regression'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_lr)),
        'MAE': mean_absolute_error(y_test, y_pred_lr),
        'R2': r2_score(y_test, y_pred_lr),
        'Predictions': y_pred_lr
    }
    models['Linear Regression'] = lr_model
    
    # Random Forest
    rf_model = RandomForestRegressor(n_estimators=100, random_state=42)
    rf_model.fit(X_train, y_train)
    y_pred_rf = rf_model.predict(X_test)
    results['Random Forest'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_rf)),
        'MAE': mean_absolute_error(y_test, y_pred_rf),
        'R2': r2_score(y_test, y_pred_rf),
        'Predictions': y_pred_rf
    }
    models['Random Forest'] = rf_model
    
    # Gradient Boosting
    gb_model = GradientBoostingRegressor(n_estimators=100, random_state=42)
    gb_model.fit(X_train, y_train)
    y_pred_gb = gb_model.predict(X_test)
    results['Gradient Boosting'] = {
        'RMSE': np.sqrt(mean_squared_error(y_test, y_pred_gb)),
        'MAE': mean_absolute_error(y_test, y_pred_gb),
        'R2': r2_score(y_test, y_pred_gb),
        'Predictions': y_pred_gb
    }
    models['Gradient Boosting'] = gb_model
    
    return models, results

def generate_visualizations(df, models, results, X_test, y_test):
    """Generate visualization plots"""
    
    # 1. Flight Delay Distribution
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Flight Delay Analysis', fontsize=16, fontweight='bold')
    
    axes[0, 0].hist(df['Delay_Minutes'], bins=50, color='steelblue', edgecolor='black')
    axes[0, 0].set_title('Delay Distribution')
    axes[0, 0].set_xlabel('Delay (minutes)')
    axes[0, 0].set_ylabel('Frequency')
    
    axes[0, 1].scatter(df['Temperature'], df['Delay_Minutes'], alpha=0.5, color='coral')
    axes[0, 1].set_title('Temperature vs Delay')
    axes[0, 1].set_xlabel('Temperature (°C)')
    axes[0, 1].set_ylabel('Delay (minutes)')
    
    axes[1, 0].scatter(df['Wind_Speed'], df['Delay_Minutes'], alpha=0.5, color='green')
    axes[1, 0].set_title('Wind Speed vs Delay')
    axes[1, 0].set_xlabel('Wind Speed (km/h)')
    axes[1, 0].set_ylabel('Delay (minutes)')
    
    axes[1, 1].scatter(df['Airport_Congestion'], df['Delay_Minutes'], alpha=0.5, color='purple')
    axes[1, 1].set_title('Airport Congestion vs Delay')
    axes[1, 1].set_xlabel('Congestion (%)')
    axes[1, 1].set_ylabel('Delay (minutes)')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/flight_delay_analysis.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 2. Model Performance Comparison
    fig, ax = plt.subplots(figsize=(12, 6))
    
    metrics = ['RMSE', 'MAE', 'R2']
    x = np.arange(len(metrics))
    width = 0.25
    
    for i, (model_name, result) in enumerate(results.items()):
        values = [result['RMSE'], result['MAE'], result['R2']]
        ax.bar(x + i*width, values, width, label=model_name)
    
    ax.set_xlabel('Metrics', fontweight='bold')
    ax.set_ylabel('Values', fontweight='bold')
    ax.set_title('Model Performance Comparison', fontweight='bold', fontsize=14)
    ax.set_xticks(x + width)
    ax.set_xticklabels(metrics)
    ax.legend()
    ax.grid(axis='y', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/flight_model_comparison.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 3. Predictions vs Actual
    fig, axes = plt.subplots(1, 3, figsize=(16, 4))
    fig.suptitle('Predictions vs Actual Values', fontsize=14, fontweight='bold')
    
    for idx, (model_name, result) in enumerate(results.items()):
        axes[idx].scatter(y_test, result['Predictions'], alpha=0.5, color='steelblue')
        axes[idx].plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--', lw=2)
        axes[idx].set_title(f'{model_name}')
        axes[idx].set_xlabel('Actual Delay')
        axes[idx].set_ylabel('Predicted Delay')
        axes[idx].grid(alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/flight_predictions_vs_actual.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 4. Feature Importance (Random Forest)
    rf_model = models['Random Forest']
    feature_importance = pd.DataFrame({
        'Feature': X_test.columns,
        'Importance': rf_model.feature_importances_
    }).sort_values('Importance', ascending=False)
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.barh(feature_importance['Feature'][:10], feature_importance['Importance'][:10], color='steelblue')
    ax.set_xlabel('Importance', fontweight='bold')
    ax.set_title('Top 10 Feature Importance (Random Forest)', fontweight='bold', fontsize=12)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/flight_feature_importance.png', dpi=300, bbox_inches='tight')
    plt.close()
    
    # 5. Weather Impact Analysis
    fig, axes = plt.subplots(2, 2, figsize=(12, 10))
    fig.suptitle('Weather Impact on Flight Delays', fontsize=14, fontweight='bold')
    
    axes[0, 0].scatter(df['Temperature'], df['Delay_Minutes'], alpha=0.4, color='red')
    axes[0, 0].set_title('Temperature Impact')
    axes[0, 0].set_xlabel('Temperature (°C)')
    axes[0, 0].set_ylabel('Delay (min)')
    
    axes[0, 1].scatter(df['Humidity'], df['Delay_Minutes'], alpha=0.4, color='blue')
    axes[0, 1].set_title('Humidity Impact')
    axes[0, 1].set_xlabel('Humidity (%)')
    axes[0, 1].set_ylabel('Delay (min)')
    
    axes[1, 0].scatter(df['Visibility'], df['Delay_Minutes'], alpha=0.4, color='green')
    axes[1, 0].set_title('Visibility Impact')
    axes[1, 0].set_xlabel('Visibility (km)')
    axes[1, 0].set_ylabel('Delay (min)')
    
    axes[1, 1].scatter(df['Precipitation'], df['Delay_Minutes'], alpha=0.4, color='purple')
    axes[1, 1].set_title('Precipitation Impact')
    axes[1, 1].set_xlabel('Precipitation (mm)')
    axes[1, 1].set_ylabel('Delay (min)')
    
    plt.tight_layout()
    plt.savefig('/home/ubuntu/flight_weather_impact.png', dpi=300, bbox_inches='tight')
    plt.close()

def main():
    print("Generating flight delay dataset...")
    df = generate_flight_data()
    df.to_csv('/home/ubuntu/flight_delay_data.csv', index=False)
    print(f"Dataset shape: {df.shape}")
    
    # Prepare features and target
    X = df.drop(['Flight_Number', 'Delay_Minutes', 'Is_Delayed'], axis=1)
    y = df['Delay_Minutes']
    
    # Split data
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Scale features
    scaler = StandardScaler()
    X_train_scaled = scaler.fit_transform(X_train)
    X_test_scaled = scaler.transform(X_test)
    
    X_train_scaled = pd.DataFrame(X_train_scaled, columns=X.columns)
    X_test_scaled = pd.DataFrame(X_test_scaled, columns=X.columns)
    
    # Train models
    print("Training models...")
    models, results = train_models(X_train_scaled, X_test_scaled, y_train, y_test)
    
    # Save results
    results_df = pd.DataFrame({
        'Model': results.keys(),
        'RMSE': [r['RMSE'] for r in results.values()],
        'MAE': [r['MAE'] for r in results.values()],
        'R2': [r['R2'] for r in results.values()]
    })
    results_df.to_csv('/home/ubuntu/flight_model_results.csv', index=False)
    print("\nModel Results:")
    print(results_df)
    
    # Generate visualizations
    print("Generating visualizations...")
    generate_visualizations(df, models, results, X_test_scaled, y_test)
    
    print("\nAll files generated successfully!")

if __name__ == "__main__":
    main()
