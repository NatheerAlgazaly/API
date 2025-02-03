// التحكم في التنقل بين النماذج
document.getElementById('btnRating').addEventListener('click', () => {
    document.getElementById('ratingSection').style.display = 'block';
    document.getElementById('popularitySection').style.display = 'none';
    document.getElementById('recommendationSection').style.display = 'none';
});

document.getElementById('btnPopularity').addEventListener('click', () => {
    document.getElementById('ratingSection').style.display = 'none';
    document.getElementById('popularitySection').style.display = 'block';
    document.getElementById('recommendationSection').style.display = 'none';
});

document.getElementById('btnRecommendation').addEventListener('click', () => {
    document.getElementById('ratingSection').style.display = 'none';
    document.getElementById('popularitySection').style.display = 'none';
    document.getElementById('recommendationSection').style.display = 'block';
});

// التنبؤ بنسبة التقييمات
document.getElementById('ratingForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    formData.append('model_type', 'rating'); // تحديد نوع النموذج

    fetch('/predict', {
        method: 'POST',
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('ratingResult').innerHTML = `<p>${data.error}</p>`;
        } else {
            document.getElementById('ratingResult').innerHTML = `
                <p><strong>التنبؤ بنسبة التقييمات:</strong> ${data.rating_prediction}%</p>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('ratingResult').innerHTML = '<p>حدث خطأ. يرجى المحاولة مرة أخرى.</p>';
    });
});

// التنبؤ بشعبية اللعبة
document.getElementById('popularityForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    formData.append('model_type', 'popularity'); // تحديد نوع النموذج

    fetch('/predict', {
        method: 'POST',
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('popularityResult').innerHTML = `<p>${data.error}</p>`;
        } else {
            document.getElementById('popularityResult').innerHTML = `
                <p><strong>التنبؤ بشعبية اللعبة:</strong> ${data.popularity_prediction}</p>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('popularityResult').innerHTML = '<p>حدث خطأ. يرجى المحاولة مرة أخرى.</p>';
    });
});

// التوصيات بناءً على الأنواع
document.getElementById('recommendationForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const formData = new FormData(this);
    formData.append('model_type', 'recommendation'); // تحديد نوع النموذج

    fetch('/predict', {
        method: 'POST',
        body: new URLSearchParams(formData)
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            document.getElementById('recommendationResult').innerHTML = `<p>${data.error}</p>`;
        } else {
            document.getElementById('recommendationResult').innerHTML = `
                <p><strong>التوصيات:</strong> ${data.recommended_games.join(', ')}</p>
            `;
        }
    })
    .catch(error => {
        console.error('Error:', error);
        document.getElementById('recommendationResult').innerHTML = '<p>حدث خطأ. يرجى المحاولة مرة أخرى.</p>';
    });
});