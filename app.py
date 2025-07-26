from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.secret_key = 'secret!'  # بۆ پرۆداکشن ئەمە بنێ بە شتەکی نهێنی و دروست
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# دروستکردنی مۆدێلی داتابەیس (جەدوال)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'

# گۆڕینی داتابەیس (دروستکردنی جەدوالەکان)
with app.app_context():
    db.create_all()

# ڕووتی سادە بۆ زیادکردنی یوزەر نوێ
@app.route('/add_user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added!"}), 201

# ڕووتی سادە بۆ وەرگرتنی هەموو یوزەرەکان
@app.route('/users')
def users():
    all_users = User.query.all()
    result = []
    for user in all_users:
        result.append({"id": user.id, "username": user.username, "email": user.email})
    return jsonify(result)

# لیستی شوێنەکان (places) کە هەمان شت لە template دەتوانرێت بەکاربهێنرێت
places = [
    {
        "id": 1,
        "name": {"en": "Ranya Park", "ku": "پارکی ڕانیە", "ar": "حديقة رانية"},
        "category": "Park",
        "price": "Free",
        "location": "Ranya Center",
        "image": "ranya_park.jpg"
    },
    {
        "id": 2,
        "name": {"en": "Lake Villa", "ku": "دۆڵی شەهیدان", "ar": "فيلا البحيرة"},
        "category": "Villa",
        "price": "$50/night",
        "location": "سەنگەسەر",
        "image": "lake_villa.jpg"
    },
    {
        "id": 3,
        "name": {"en": "Mountain Cafe", "ku": "کافێ 64", "ar": "مقهى الجبل"},
        "category": "Cafe",
        "price": "$5",
        "location": "ڕانییە-نەورۆز",
        "image": "mountain_cafe.jpg"
         },
    {
        "id": 4,
        "name": {"en": "Villa 64", "ku": "ڤێلا ٦٤", "ar": "فيلا ٦٤"},
        "category": "Villa",
        "price": "$75/night",
        "location": "سەرکەپکان",
        "image": "villa64.jpg"
    },
    {
        "id": 5,
        "name": {"en": "Fenik Park", "ku": "سەیرانگای فێنک", "ar": "منتزه فينيك"},
        "category": "Park",
        "price": "$30",
        "location": "هەڵشۆ",
        "image": "fenik_park.jpg"
    },
    {
        "id": 6,
        "name": {"en": "Soli Dewjan", "ku": "سولی دەوژان", "ar": "سولي دوجان"},
        "category": "Park",
        "price": "$10",
        "location": "قەڵادزێ",
        "image": "soli_dewjan.jpg"
    },
    {
        "id": 7,
        "name": {"en": "Derband Safari", "ku": "دەربەند سەفاری", "ar": "دربند سفاري"},
        "category": "Park",
        "price": "$10",
        "location": "دەربەند",
        "image": "derband_safari.jpg"
    },
    {
        "id": 8,
        "name": {"en": "Ranya Safari", "ku": "ڕانییە سەفاری", "ar": "رانيا سفاري"},
        "category": "Park",
        "price": "$10",
        "location": "ڕانیە",
        "image": "ranya_safari.jpg"
    },
    {
        "id": 9,
        "name": {"en": "Koikha Restaurant", "ku": "ڕێستۆرانتی کوێخا", "ar": "مطعم كوخيها"},
        "category": "Cafe",
        "price": "$20 avg",
        "location": "دۆڵی شاورێ",
        "image": "koikha_restaurant.jpg"
    },
    {
        "id": 10,
        "name": {"en": "Deman Park", "ku": "سەیرانگای دێمان", "ar": "منتزه ديمان"},
        "category": "Park",
        "price": "$25",
        "location": "دۆڵی شاورێ",
        "image": "deman_park.jpg"
    },
    {
        "id": 11,
        "name": {"en": "Kawben Park", "ku": "سەیرانگای کەوبێن", "ar": "منتزه كاوبين"},
        "category": "Park",
        "price": "$30",
        "location": "گوندی کەوبێن",
        "image": "kawben_park.jpg"
    },
    {
        "id": 12,
        "name": {"en": "Zini Werte", "ku": "زینی وەرتێ", "ar": "زيني ويرتي"},
        "category": "Park",
        "price": "$5",
        "location": "وەرتێ",
        "image": "zini_werte.jpg"
    },
    {
        "id": 13,
        "name": {"en": "Shahur Restaurant", "ku": "ڕێستۆرانتی شاهور", "ar": "مطعم شاهور"},
        "category": "Cafe",
        "price": "$15 avg",
        "location": "دۆڵی شاورێ",
        "image": "shahur_restaurant.jpg"
    },
]

def get_locale():
    # گرتنی زمان لە پارامێتەر یان سێشن یان بە یەکێکی تر (ئەگەر هەبوو)
    lang = request.args.get('lang')
    if lang:
        session['lang'] = lang
    return session.get('lang', 'ku')  # بە پیشەنی کوردی

@app.route('/set_language/<language>')
def set_language(language):
    session['lang'] = language
    return redirect(request.referrer or url_for('index'))

@app.route('/')
def index():
    lang = get_locale()
    category = request.args.get('category')
    filtered_places = places

    if category:
        filtered_places = [p for p in places if p['category'].lower() == category.lower()]

    return render_template('index.html', places=filtered_places, lang=lang)

@app.route('/contact')
def contact():
    lang = get_locale()
    return render_template('contact.html', lang=lang)
@app.route('/register', methods=['GET', 'POST'])
def register():
    lang = get_locale()
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        # لە راستی پێویستە password hash بکەیت
        user = User(username=username, email=email)
        db.session.add(user)
        db.session.commit()
        flash("تۆمارکراوە بە سەرکەوتوویی!", "success")
        return redirect(url_for('login'))

    return render_template('register.html', lang=lang)

@app.route('/place/<int:place_id>')
def place_detail(place_id):
    lang = get_locale()
    place = next((p for p in places if p['id'] == place_id), None)
    if place:
        return render_template('place_detail.html', place=place, lang=lang)
    else:
        return "Place not found", 404
@app.route('/rent/<int:place_id>', methods=['GET', 'POST'])
def rent_place(place_id):
    lang = get_locale()
    place = next((p for p in places if p['id'] == place_id), None)
    if not place:
        return "Place not found", 404

    if request.method == 'POST':
        name = request.form['name']
        phone = request.form['phone']
        date = request.form['date']

        flash(f"سوپاس {name}! شوێنەکەت بە کرێ گرت بۆ ڕۆژی {date}.")
        return redirect(url_for('place_detail', place_id=place_id))

    return render_template('rent.html', place=place, lang=lang)


@app.route('/login', methods=['GET', 'POST'])
def login():
    lang = get_locale()
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user'] = user.username
            flash("چوونەژوورەوە بە سەرکەوتوویی کرد", "success")
            return redirect(url_for('index'))
        else:
            flash("ئیمەیڵ یان وشەی نهێنی هەڵەیە", "error")
    return render_template('login.html', lang=lang)
@app.route('/logout')
def logout():
    session.pop('user', None)
    flash("چوونەدەرەوە کرا", "info")
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)