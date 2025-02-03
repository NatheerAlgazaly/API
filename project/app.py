from flask import Flask, render_template, request, jsonify
import joblib
import numpy as np
import pandas as pd

# إنشاء تطبيق Flask
app = Flask(__name__)

# تحميل النماذج
model_rf = joblib.load('models/rating_prediction_model.pkl')  # RandomForestRegressor
model_hgb = joblib.load('models/popularity_prediction_model.pkl')  # HistGradientBoostingClassifier
mlb = joblib.load('models/genres_encoder.pkl')  # OneHotEncoder
pipeline_knn = joblib.load('models/recommendation_model.pkl')  # KNN

# الصفحة الرئيسية
@app.route('/')
def home():
    return render_template('index.html')

# معالجة طلب التنبؤ
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # تحديد نوع النموذج
        model_type = request.form.get('model_type')

        if model_type == 'rating':
            # جمع البيانات المدخلة لنموذج التقييمات
            total_reviews = request.form.get('total_reviews')
            total_positive = request.form.get('total_positive')
            total_negative = request.form.get('total_negative')
            n_achievements = request.form.get('n_achievements')
            required_age = request.form.get('required_age')

            # التحقق من وجود جميع الحقول
            if not all([total_reviews, total_positive, total_negative, n_achievements, required_age]):
                return jsonify({'error': 'بعض الحقول مفقودة. يرجى التأكد من إدخال جميع البيانات.'})

            # تحويل القيم إلى الأنواع المناسبة
            total_reviews = float(total_reviews)
            total_positive = float(total_positive)
            total_negative = float(total_negative)
            n_achievements = float(n_achievements)
            required_age = float(required_age)

            # التنبؤ بتقييمات اللعبة
            input_data = np.array([[total_reviews, total_positive, total_negative, n_achievements, required_age]])
            rating_prediction = model_rf.predict(input_data)[0]

            # إرجاع النتائج
            return jsonify({
                'rating_prediction': round(rating_prediction, 2)
            })

        elif model_type == 'popularity':
            # جمع البيانات المدخلة لنموذج الشعبية
            total_reviews = request.form.get('total_reviews')
            total_positive = request.form.get('total_positive')
            total_negative = request.form.get('total_negative')
            n_achievements = request.form.get('n_achievements')
            release_date = request.form.get('release_date')

            # التحقق من وجود جميع الحقول
            if not all([total_reviews, total_positive, total_negative, n_achievements, release_date]):
                return jsonify({'error': 'بعض الحقول مفقودة. يرجى التأكد من إدخال جميع البيانات.'})

            # تحويل القيم إلى الأنواع المناسبة
            total_reviews = float(total_reviews)
            total_positive = float(total_positive)
            total_negative = float(total_negative)
            n_achievements = float(n_achievements)
            release_date = pd.to_datetime(release_date)
            age = (pd.Timestamp.now() - release_date).days / 365

            # التنبؤ بعمر اللعبة قبل أن تصبح غير شائعة
            popularity_input = np.array([[age, total_reviews, total_positive, total_negative, n_achievements]])
            popularity_prediction = model_hgb.predict(popularity_input)[0]
            popularity_label = "شائعة" if popularity_prediction == 1 else "غير شائعة"

            # إرجاع النتائج
            return jsonify({
                'popularity_prediction': popularity_label
            })

        elif model_type == 'recommendation':
            # جمع البيانات المدخلة لنموذج التوصيات
            total_reviews = request.form.get('total_reviews')
            total_positive = request.form.get('total_positive')
            total_negative = request.form.get('total_negative')
            n_achievements = request.form.get('n_achievements')
            genres = request.form.get('genres')

            # التحقق من وجود جميع الحقول
            if not all([total_reviews, total_positive, total_negative, n_achievements, genres]):
                return jsonify({'error': 'بعض الحقول مفقودة. يرجى التأكد من إدخال جميع البيانات.'})

            # تحويل القيم إلى الأنواع المناسبة
            total_reviews = float(total_reviews)
            total_positive = float(total_positive)
            total_negative = float(total_negative)
            n_achievements = float(n_achievements)

            # التوصيات بناءً على الأنواع
            input_recommendation = pd.DataFrame({
                'total_reviews': [total_reviews],
                'total_positive': [total_positive],
                'total_negative': [total_negative],
                'n_achievements': [n_achievements],
                'genres': [genres]
            })
            distances, indices = pipeline_knn.named_steps['knn'].kneighbors(
                pipeline_knn.named_steps['preprocessor'].transform(input_recommendation)
            )
            recommended_games = indices.flatten()[1:]  # استبعاد اللعبة نفسها

            # إرجاع النتائج
            return jsonify({
                'recommended_games': recommended_games.tolist()
            })

        else:
            return jsonify({'error': 'نوع النموذج غير صالح.'})

    except Exception as e:
        return jsonify({'error': str(e)})

# تشغيل التطبيق
if __name__ == '__main__':
    app.run(debug=True)