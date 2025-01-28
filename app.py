from flask import Flask, render_template
import pandas as pd
import json

app = Flask(__name__)

def load_data():
    df = pd.read_csv('spark_streaming_prediction.csv')
    df['prediction'] = df['prediction'].map({0: 'Clean', 1: 'Harmful'})
    return df

@app.route('/')
def dashboard():
    df = load_data()
    
    total_comments = len(df)
    prediction_counts = df['prediction'].value_counts().to_dict()
    
    # Lấy 20 comment cho mỗi nhãn
    clean_comments = df[df['prediction'] == 'Clean']['joined_words'].head(20).tolist()
    hate_comments = df[df['prediction'] == 'Harmful']['joined_words'].head(20).tolist()
    
    chart_data = [
        {'name': label, 'value': count} 
        for label, count in prediction_counts.items()
    ]
    
    return render_template(
        'dashboard.html',
        total_comments=total_comments,
        prediction_counts=prediction_counts,
        chart_data=json.dumps(chart_data),
        clean_comments=clean_comments,
        hate_comments=hate_comments
    )

if __name__ == '__main__':
    app.run(debug=True)