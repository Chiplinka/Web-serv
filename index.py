from flask import Flask, session, redirect, render_template, flash, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from models import UsersModel, BooksModel, LibraryModel
from forms import LoginForm, RegisterForm, AddbookForm, SearchPriceForm, SearchDealerForm, AddDealerForm
from db import DB

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'
db = DB()
UsersModel(
    db.get_connection()).init_table()
BooksModel(db.get_connection()).init_table()
LibraryModel(db.get_connection()).init_table()


@app.route('/')
@app.route('/index')
def index():
    if 'username' not in session:
        return redirect('/login')
    # если админ, то его на свою страницу
    if session['username'] == 'admin':
        return render_template('index_admin.html', username=session['username'])
    # если обычный пользователь, то его на свою
    cars = BooksModel(db.get_connection()).get_all()
    return render_template('book_user.html', username=session['username'], title='Просмотр базы', cars=cars)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Страница авторизации
    :return:
    переадресация на главную, либо вывод формы авторизации
    """
    form = LoginForm()
    if form.validate_on_submit():  # ввели логин и пароль
        user_name = form.username.data
        password = form.password.data
        user_model = UsersModel(db.get_connection())
        # проверяем наличие пользователя в БД и совпадение пароля
        if user_model.exists(user_name)[0] and check_password_hash(user_model.exists(user_name)[1], password):
            session['username'] = user_name  # запоминаем в сессии имя пользователя и кидаем на главную
            return redirect('/index')
        else:
            flash('Пользователь или пароль не верны')
    return render_template('login.html', title='Авторизация', form=form)


@app.route('/logout')
def logout():

    session.pop('username', 0)
    return redirect('/login')


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():

        users = UsersModel(db.get_connection())
        if form.user_name.data in [u[1] for u in users.get_all()]:
            flash('Такой пользователь уже существует')
        else:
            users.insert(user_name=form.user_name.data, email=form.email.data,
                         password_hash=generate_password_hash(form.password_hash.data))
            return redirect(url_for('index'))
    return render_template("register.html", title='Регистрация пользователя', form=form)



@app.route('/book_admin', methods=['GET'])
def book_admin():
    if 'username' not in session:
        return redirect('/login')

    if session['username'] != 'admin':
        flash('Доступ запрещен')
        return redirect('/index')

    cars = BooksModel(db.get_connection()).get_all()
    return render_template('book_admin.html',
                           username=session['username'],
                           title='Просмотр автомобилей',
                           cars=cars)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():

    if 'username' not in session:
        return redirect('login')

    if session['username'] != 'admin':
        return redirect('index')
    form = AddbookForm()
    available_library = [(i[0], i[1]) for i in LibraryModel(db.get_connection()).get_all()]
    form.library_id.choices = available_library
    if form.validate_on_submit():

        cars = BooksModel(db.get_connection())
        cars.insert(name=form.name.data,
                    price=form.price.data,
                    info=form.info.data,
                    library=form.library_id.data )

        return redirect(url_for('book_admin'))
    return render_template("add_book.html", title='Добавление книги', form=form)


@app.route('/book/<int:book_id>', methods=['GET'])
def book(book_id):

    if 'username' not in session:
        return redirect('/login')

    '''if session['username'] != 'admin':
        return redirect(url_for('index'))'''

    car = BooksModel(db.get_connection()).get(book_id)
    dealer = LibraryModel(db.get_connection()).get(car[4])
    return render_template('book_info.html',
                           username=session['username'],
                           title='Просмотр автомобиля',
                           car=car,
                           dealer=dealer[1])


@app.route('/search_price', methods=['GET', 'POST'])
def search_price():

    form = SearchPriceForm()
    if form.validate_on_submit():

        cars = BooksModel(db.get_connection()).get_by_price(form.start_price.data, form.end_price.data)

        return render_template('book_user.html', username=session['username'], title='Просмотр базы', cars=cars)
    return render_template("search_price.html", title='Подбор по цене', form=form)


@app.route('/search_library', methods=['GET', 'POST'])
def search_library():

    form = SearchDealerForm()
    available_dealers = [(i[0], i[1]) for i in LibraryModel(db.get_connection()).get_all()]
    form.library_id.choices = available_dealers
    if form.validate_on_submit():
        cars = BooksModel(db.get_connection()).get_by_dealer(form.library_id.data)
        return render_template('book_user.html', username=session['username'], title='Просмотр базы', cars=cars)
    return render_template("search_library.html", title='Подбор по цене', form=form)


'''Работа с дилерским центром'''


@app.route('/library_admin', methods=['GET'])
def library_admin():

    if 'username' not in session:
        return redirect('/login')

    if session['username'] != 'admin':
        flash('Доступ запрещен')
        redirect('/index')

    dealers = LibraryModel(db.get_connection()).get_all()
    return render_template('library_admin.html',
                           username=session['username'],
                           title='Просмотр Дилерских центров',
                           dealers=dealers)


@app.route('/dealer/<int:dealer_id>', methods=['GET'])
def dealer(dealer_id):
    if 'username' not in session:
        return redirect('/login')

    if session['username'] != 'admin':
        return redirect(url_for('index'))
    dealer = LibraryModel(db.get_connection()).get(dealer_id)
    return render_template('dealer_info.html',
                           username=session['username'],
                           title='Просмотр информации о дилерском центре',
                           dealer=dealer)


@app.route('/add_library', methods=['GET', 'POST'])
def add_library():
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'admin':
        form = AddDealerForm()
        if form.validate_on_submit():
            dealers = LibraryModel(db.get_connection())
            dealers.insert(name=form.name.data, address=form.address.data)
            return redirect(url_for('library_admin'))
        return render_template("add_library.html", title='Добавление дилерского центра', form=form)


@app.route('/del_book/<int:book_id>', methods=['GET'])
def del_fruit(book_id):
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'admin':
        car = BooksModel(db.get_connection())
        car.delete(book_id)
        return redirect(url_for('book_admin'))
    else:
        return redirect(url_for('index'))

@app.route('/del_library/<int:library_id>', methods=['GET'])
def del_library(library_id):
    if 'username' not in session:
        return redirect('/login')
    if session['username'] == 'admin':
        library = LibraryModel(db.get_connection())
        library.delete(library_id)
        books = BooksModel(db.get_connection())
        books.get_delete_by_library_id(library_id)
        return redirect(url_for('library_admin'))
    else:
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
