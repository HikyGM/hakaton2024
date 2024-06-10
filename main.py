import json
import os
import datetime
import matplotlib.pyplot as plt
from random import randint, randrange, choices, choice

from flask import Flask, render_template, redirect
from flask_login import LoginManager, login_user, login_required, logout_user, current_user

from forms.user import RegisterForm, LoginForm, EditPasswordForm, EditForm
from forms.problem_form import EquationsForm, ComplexsForm, TaskForm

from data import db_session
from data.users import User
from data.score import Score
from data.difficulty_levels import Difficulty_levels

import generators
import informations

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)
app.config['SECRET_KEY'] = '98765redcvbnmlo9876trfcdr56yuhgr5yhbvcdertyu'
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=365)
alphabet = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'


@app.errorhandler(401)
def custom_401(error):
    """
    Пользовательский обработчик ошибок для неавторизованных ошибок HTTP 401.

    Эта функция является обработчиком ошибок, который запускается при возникновении неавторизованной ошибки 401.
    Она перенаправляет пользователя на страницу "/login".

    Параметры:
        ошибка (Exception): объект exception, представляющий ошибку 401.

    Возвращается:
        Ответ: Ответ на перенаправление на страницу "/login".
    """
    return redirect("/login")


@login_manager.user_loader
def load_user(user_id):
    """
    Загрузка объекта пользователя на основе предоставленного идентификатора.

    Параметры:
        user_id (int): идентификатор загружаемого пользователя.

    Возвращается:
        Пользователь: загруженный пользовательский объект или None, если пользователь не найден.

    """
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/register', methods=['GET', 'POST'])
def reqister():
    """
        Регистрирует нового пользователя в системе.

        Эта функция выполняет регистрацию нового пользователя в системе.
        Доступ к ней осуществляется по маршруту "/register" с помощью методов "GET" и "POST".

        Параметры:
            Нет

        Возвращается:
            - Если регистрационная форма заполнена и пароли совпадают,
                функция создает нового пользователя в базе данных с указанным именем пользователя и электронной почтой.
                Также создается запись о набранных баллах для каждого уровня сложности.
                Затем пользователь перенаправляется на страницу "/login".

            - Если регистрационная форма отправлена,
                но пароли не совпадают,
                функция отображает шаблон 'pages-register.html с сообщением об ошибке "Вы не согласны".

            - Если регистрационная форма отправлена,
                но пользователь с таким же адресом электронной почты уже существует в базе данных,
                функция отображает 'pages-register.html шаблон с названием "Регистрация",
                регистрационной формой и сообщением об ошибке "Такой пользователь здесь".

            - Если регистрационная форма не отправлена,
                возвращается шаблон "pages-register.html" с заголовком "Регистрация" и регистрационной формой.

    """
    form = RegisterForm()
    if form.validate_on_submit():
        if form.password.data != form.password_again.data:
            return render_template('pages-register.html', title='Регистрация', form=form,
                                   message="Пароли не совпадают")
        db_sess = db_session.create_session()
        if db_sess.query(User).filter(User.email == form.email.data).first():
            return render_template('pages-register.html', title='Регистрация', form=form,
                                   message="Такой пользователь уже есть")

        user = User(
            name=form.username.data,
            email=form.email.data,
        )
        user.set_password(form.password.data)
        db_sess.add(user)
        db_sess.commit()

        difficulty_levels = db_sess.query(Difficulty_levels).all()

        for difficulty_level in difficulty_levels:
            score = Score(user_id=user.id, difficulty_levels_id=difficulty_level.id)
            db_sess.add(score)
            db_sess.commit()

        return redirect('/login')
    return render_template('pages-register.html', title='Регистрация', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    """
        Маршрут для обработки входа пользователя в систему.

        Эта функция обрабатывает процесс входа для существующих пользователей.

        Она берет данные формы из формы входа в систему и проверяет их.

        Если данные формы верны, программа запрашивает базу данных, чтобы проверить,
            есть ли пользователь с указанным адресом электронной почты.

        Если пользователь найден и пароль совпадает, пользователь
            входит в систему и перенаправляется на страницу панели мониторинга.

        Если вход не удался, выводится сообщение об ошибке отображается на странице входа в систему.

        Если данные формы неверны,
            на странице входа в систему отображаются указанные данные формы и сообщение об ошибке.

        Параметры:
            Никто

        Возвращается:
            Если вход в систему выполнен успешно, пользователь перенаправляется на страницу панели мониторинга.
            Если вход в систему выполнен неудачно, возвращается шаблон "pages-login.html" с сообщением об ошибке
                и предоставленными данными формы.
    """
    form = LoginForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.email == form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect("/dashboard")
        return render_template('pages-login.html', message="Неправильный логин или пароль", form=form)
    return render_template('pages-login.html', title='Авторизация', form=form)


@app.route('/logout')
@login_required
def logout():
    """
        Завершает работу с текущим пользователем, вызывая функцию `logout_user()` из расширения Flask-Login.
        Перенаправляет пользователя на домашнюю страницу ("/") после выхода из системы.

        Этот маршрут помечен как "@login_required", что означает,
            что доступ к этому маршруту могут получить только прошедшие проверку подлинности пользователи.

        Возвращается:
            Перенаправление на домашнюю страницу ("/").
    """
    logout_user()
    return redirect("/")


@app.route("/profile", methods=['GET', 'POST'])
@login_required
def profile():
    """
        Маршрут для страницы профиля пользователя.

        Эта функция обрабатывает запросы GET и POST на маршрут "/profile".
        Она извлекает оценку пользователя из базы данных и вычисляет рейтинг пользователя на основе общего балла.
        Он также обрабатывает отправку форм для редактирования пароля пользователя и информации профиля.
        Возвращается:
            - Если отправлена форма для редактирования пароля,
                обновляется пароль пользователя в базе данных и перенаправляет на страницу профиля.
            - Если отправлена форма для редактирования информации профиля,
                обновляется информация профиля пользователя в базе данных и перенаправляет на страницу профиля.
            - В противном случае отображается страница профиля с информацией пользователя и активной вкладкой.
    """
    db_sess = db_session.create_session()
    form_edit_password = EditPasswordForm()

    form_edit = EditForm()

    score = db_sess.query(Score).filter(Score.user_id == current_user.id).all()

    total = sum(item.level_rate * item.difficulty_levels.difficulty_levels_weight for item in score)

    if total <= 10:
        rank = 'Рекрут'
    elif total <= 100:
        rank = 'Страж'
    elif total <= 1000:
        rank = 'Рыцарь'
    elif total <= 10000:
        rank = 'Герой'
    elif total <= 100000:
        rank = 'Легенда'
    elif total <= 1000000:
        rank = 'Властелин'
    elif total <= 10000000:
        rank = 'Божество'
    else:
        rank = 'Титан'

    param = {
        'template_name_or_list': 'profile.html',
        'title': 'Профиль',
        'form_edit': form_edit,
        'form_edit_password': form_edit_password,
        'rank': rank,

        'level_all': sum([item.level_all for item in score]),
        'level_rate': sum([item.level_rate for item in score]),

    }
    param['level_wrong'] = param['level_all'] - param['level_rate']

    param_active_tab_edit_password = {
        'edit_password': 'aria-selected=true tabindex=-1',
        'edit_password_active': 'active',
        'edit_password_show': 'show'
    }

    param_active_tab_my_profile = {
        'my_profile': 'aria-selected=true tabindex=-1',
        'my_profile_active': 'active',
        'my_profile_show': 'show'
    }

    active_tab = param_active_tab_my_profile

    if form_edit_password.validate_on_submit():
        active_tab = param_active_tab_edit_password
        if current_user.check_password(form_edit_password.password_check.data):
            if form_edit_password.password_new.data == form_edit_password.password_again.data:
                user = db_sess.query(User).filter(User.email == current_user.email).first()
                user.set_password(form_edit_password.password_new.data)
                db_sess.add(user)
                db_sess.commit()
                return render_template(**param, **active_tab, error_message='Успешно!')
            return render_template(**param, **active_tab, error_message='Пароли не совпадают')
        return render_template(**param, **active_tab, error_message='Неправильный пароль')

    if form_edit.validate_on_submit():
        user = db_sess.query(User).get(current_user.id)
        if form_edit.source_image.data.filename:
            if user.source_image != 'default.png':
                os.remove(f'static/assets/img/service/images_profiles_users/{user.source_image}')
            filename = f'{"".join(choices(alphabet, k=15))}.png'
            form_edit.source_image.data.save(f'static/assets/img/service/images_profiles_users/{filename}')
            user.source_image = filename

        if form_edit.username.data:
            user.name = form_edit.username.data
        if form_edit.about.data:
            user.about = form_edit.about.data
        db_sess.add(user)
        db_sess.commit()
        return redirect('/profile')

    return render_template(**param, **active_tab)


@app.route("/")
@app.route("/index")
def index():
    """
        Средство настройки маршрута для корневого URL ("/") и "индексного" URL ("/index").
        Эта функция возвращает отображаемый шаблон "index.html".
        Возвращается:
            Шаблон "index.html".
    """
    return render_template("index.html")


def render(title):
    db_sess = db_session.create_session()
    score = db_sess.query(Score).filter(Score.user_id == current_user.id).all()
    score = [item for item in score if item.difficulty_levels.difficulty_levels_type == title]
    params = json.dumps([{'value': i.level_rate, 'name': i.difficulty_levels.difficulty_levels_title} for i in score])
    return render_template("dashboard.html", score=score, params=params, title='Задачи')


@app.route("/dashboard")
@login_required
def dashboard():
    db_sess = db_session.create_session()
    score = db_sess.query(Score).filter(Score.user_id == current_user.id).all()
    score = [item for item in score if item.difficulty_levels.difficulty_levels_type == 'primer']

    users = db_sess.query(User).all()
    top_user = sorted(users, key=lambda x: x.total_score, reverse=True)[:10]
    # scores = []
    #
    # for user in users:
    #     top_score = db_sess.query(Score).filter(Score.user_id == user.id).all()
    #     total = sum(item.level_rate * item.difficulty_levels.difficulty_levels_weight for item in top_score)
    #     scores.append({'name': user.name, 'total': total})



    return render_template("main-dashboard.html", score=score, title='Главная',top_user=top_user)


@app.route("/addition")
@login_required
def dashboard_addition():
    return render('addition')


@app.route("/subtraction")
@login_required
def dashboard_subtraction():
    return render('subtraction')


@app.route("/multiplication")
@login_required
def dashboard_multiplication():
    return render('multiplication')


@app.route("/division")
@login_required
def dashboard_division():
    return render('division')


@app.route("/complex_arithmetic")
@login_required
def dashboard_complex_arithmetic():
    return render('complex_arithmetic')


@app.route("/complex")
@app.route("/equations")
@app.route("/basic_algebra")
@login_required
def dashboard_equations():
    db_sess = db_session.create_session()
    score = db_sess.query(Score).filter(Score.user_id == current_user.id).all()
    score = [item for item in score if
             item.difficulty_levels.difficulty_levels_type in {'equations', 'complex', 'basic_algebra'}]
    params = json.dumps(
        [{'value': i.level_rate, 'name': i.difficulty_levels.difficulty_levels_title, 'id': i.difficulty_levels.id} for
         i in score])
    return render_template("dashboard.html", score=score, params=params, title='Задачи')


def new_score(score):
    """
        Обновляет данный объект оценки, добавляя к нему текущую дату и время,
        увеличивает значение поля level_all на 1, удаляет файл изображения, связанный с оценкой,
        устанавливает для полей level_url_image и level_answer значение None и возвращает обновленный объект оценки.

        Параметры:
            оценка (Score): объект оценки, который будет обновлен.

        Возвращается:
            Оценка: Обновленный объект оценки.
        """
    score.level_last_date = datetime.datetime.now().strftime("%d.%m.%Y %H:%M")
    score.level_all += 1
    os.remove(f'static/sample_image/{score.level_url_image}')
    score.level_url_image = None
    score.level_answer = None
    return score


def new_score_image(score, problem, solution, db_sess, font):
    """
        Генерирует новое изображение оценки со случайно сгенерированным ответом на уровень и сохраняет его в базе данных.

        Параметры:
            оценка (Score): объект оценки, который обновляется с помощью нового ответа на уровень и изображения URL-адреса уровня.
            gen (генератор): объект генератора, используемый для генерации случайного выражения.
            db_sess (сессия): Объект сессии базы данных, используемый для добавления и фиксации объекта score.

        Возвращается:
            None

        Описание:
            - Генерирует случайный ответ уровня от 1 до 100.
            - Генерирует случайное латексное выражение, используя объект generator.
            - Задает параметры ответа на уровне и URL-адреса уровня для объекта score.
            - Добавляет объект score в сеанс базы данных.
            - Фиксирует изменения в базе данных.
            - Сохраняет сгенерированное изображение в каталоге 'static/sample_image' со случайно сгенерированным именем файла.(8, 2)
        """
    if type(solution) == str:
        score.level_answer = solution
    else:
        score.level_answer = round(solution, 2)
    plt.text(0, 0, problem, horizontalalignment='center', verticalalignment='center', fontdict=font)
    score.level_url_image = f'{"".join(choices(alphabet, k=15))}.png'
    db_sess.add(score)
    db_sess.commit()
    plt.savefig(f'static/sample_image/{score.level_url_image}')


def new_plt(figsize):
    plt.figure().clear()
    plt.figure(figsize=figsize, dpi=300)
    plt.plot()
    plt.axis("off")


def get_score(db_sess, title, _type):
    return db_sess.query(Score).filter(
        Score.user_id == current_user.id,
        Score.difficulty_levels_id == db_sess.query(Difficulty_levels).filter(
            Difficulty_levels.difficulty_levels_title == title,
            Difficulty_levels.difficulty_levels_type == _type).first().id).first()


def main_render(form, levels_title, _id, info, template):
    db_sess = db_session.create_session()
    difficulty = db_sess.query(Difficulty_levels).filter(Difficulty_levels.id == _id).first()
    score = get_score(db_sess, difficulty.difficulty_levels_title, levels_title)
    if form.validate_on_submit():
        if form.new_submit.data:
            score = new_score(score)
            db_sess.add(score)
            db_sess.commit()
            return redirect(f'/{levels_title}/{_id}')
        if form.submit.data:
            if form.x.data == str(score.level_answer):
                score = new_score(score)
                score.level_rate += 1
                print(current_user.total_score)
                current_user.total_score += score.difficulty_levels.difficulty_levels_weight
                db_sess.add(score)
                db_sess.merge(current_user)
                db_sess.commit()
                return redirect(f'/{levels_title}/{_id}')
            return render_template(template, form=form, info=info, primer=score.level_url_image,
                                   error='Неправильно', title_card=difficulty.difficulty_levels_title,
                                   date=score.level_last_date)
    if not score.level_url_image:
        if levels_title == 'addition':
            func_redirect = addition_fun
        elif levels_title == 'subtraction':
            func_redirect = subtraction_fun
        elif levels_title == 'multiplication':
            func_redirect = multiplication_fun
        elif levels_title == 'division':
            func_redirect = division_fun
        elif levels_title == 'complex_arithmetic':
            func_redirect = complex_arithmetic_func
        elif levels_title == 'basic_algebra':
            func_redirect = basic_algebra_func

        func_redirect(score, db_sess, difficulty.difficulty_levels_complexity)

    return render_template(
        template, primer=score.level_url_image, form=form, info=info,
        title=difficulty.difficulty_levels_title, title_card=difficulty.difficulty_levels_title,
        date=score.level_last_date
    )


def addition_fun(score, db_sess, levels_complexity):
    if levels_complexity == 1:
        problem, solution = generators.addition()
    elif levels_complexity == 2:
        problem, solution = generators.addition(1000, complexity=3)
    elif levels_complexity == 3:
        problem, solution = generators.addition(10000, complexity=3)
    elif levels_complexity == 4:
        problem, solution = generators.addition(100000, complexity=4)
    elif levels_complexity == 5:
        problem, solution = generators.addition(1000000, complexity=4)
    else:
        problem, solution = generators.addition(10000000, complexity=5)
    new_plt((4, 1))
    font = {'family': 'serif'}
    new_score_image(score, '$' + problem + '$', solution, db_sess, font)


def subtraction_fun(score, db_sess, levels_complexity):
    if levels_complexity == 1:
        problem, solution = generators.subtraction()
    elif levels_complexity == 2:
        problem, solution = generators.subtraction(1000, 700, complexity=3)
    elif levels_complexity == 3:
        problem, solution = generators.subtraction(10000, 7000, complexity=3)
    elif levels_complexity == 4:
        problem, solution = generators.subtraction(100000, 70000, complexity=4)
    elif levels_complexity == 5:
        problem, solution = generators.subtraction(1000000, 700000, complexity=4)
    else:
        problem, solution = generators.subtraction(10000000, 7000000, complexity=5)
    new_plt((2, 1))
    font = {'family': 'serif'}
    new_score_image(score, '$' + problem + '$', solution, db_sess, font)


def multiplication_fun(score, db_sess, levels_complexity):
    if levels_complexity == 1:
        problem, solution = generators.multiplication()
    elif levels_complexity == 2:
        problem, solution = generators.multiplication(complexity=3)
    elif levels_complexity == 3:
        problem, solution = generators.multiplication(50, complexity=3)
    elif levels_complexity == 4:
        problem, solution = generators.multiplication(50, complexity=4)
    elif levels_complexity == 5:
        problem, solution = generators.multiplication(100, complexity=4)
    else:
        problem, solution = generators.multiplication(100, complexity=5)
    new_plt((2, 1))
    font = {'family': 'serif'}
    new_score_image(score, '$' + problem + '$', solution, db_sess, font)


def division_fun(score, db_sess, levels_complexity):
    if levels_complexity == 1:
        problem, solution = generators.division()
    elif levels_complexity == 2:
        problem, solution = generators.division(complexity=3)
    elif levels_complexity == 3:
        problem, solution = generators.division(50, complexity=3)
    elif levels_complexity == 4:
        problem, solution = generators.division(50, complexity=4)
    elif levels_complexity == 5:
        problem, solution = generators.division(100, complexity=4)
    else:
        problem, solution = generators.division(100, complexity=5)
    new_plt((2, 1))
    font = {'family': 'serif'}
    new_score_image(score, '$' + problem + '$', solution, db_sess, font)


def basic_algebra_func(score, db_sess, levels_complexity):
    problem, solution = generators.basic_algebra()
    new_plt((2, 1))
    font = {'family': 'serif'}
    new_score_image(score, '$' + problem + '$', solution, db_sess, font)


def composite_frac():
    problem_1, solution_1 = choice(problems_2)()
    while solution_1 == 0:
        problem_1, solution_1 = choice(problems_2)()
    problem_2, solution_2 = choice(problems_2)()
    while solution_2 == 0:
        problem_2, solution_2 = choice(problems_2)()
    return rf'\frac{{{problem_1}}}{{{problem_2}}}', solution_1 / solution_2


def composite_root():
    problem_1, solution_1 = choice(problems_6)()
    while solution_1 == 0:
        problem_1, solution_1 = choice(problems_6)()
    problem_2, solution_2 = generators.cube_root()
    while solution_2 == 0:
        problem_2, solution_2 = generators.cube_root()
    problem = rf'({problem_1})^{problem_2}'
    solution = solution_1 ** solution_2
    return problem, solution


problems_1 = [
    generators.division, generators.addition, generators.multiplication, generators.subtraction
]

problems_2 = problems_1 + [composite_frac, generators.factorial]

problems_3 = problems_2 + [generators.cube_root, generators.square_root, generators.log]

problems_4 = problems_3 + [generators.square, generators.divide_fractions]

problems_5 = problems_4 + [generators.fraction_multiplication, generators.simplify_square_root]

problems_6 = problems_5 + [composite_root, composite_frac, composite_frac]


def complex_arithmetic_func(score, db_sess, levels_complexity):
    if levels_complexity == 1:
        problem, solution = choice(problems_1)()
        for i in range(1):
            current_problem, current_solution = choice(problems_1)()
            solution += current_solution
            problem += '+' + current_problem
    elif levels_complexity == 2:
        problem, solution = choice(problems_2)()
        for i in range(2):
            current_problem, current_solution = choice(problems_2)()
            solution += current_solution
            problem += '+' + current_problem
    elif levels_complexity == 3:
        problem, solution = choice(problems_3)()
        for i in range(3):
            current_problem, current_solution = choice(problems_3)()
            solution += current_solution
            problem += '+' + current_problem
    elif levels_complexity == 4:
        problem, solution = choice(problems_4)()
        for i in range(4):
            current_problem, current_solution = choice(problems_4)()
            solution += current_solution
            problem += '+' + current_problem
    elif levels_complexity == 5:
        problem, solution = choice(problems_5)()
        for i in range(5):
            current_problem, current_solution = choice(problems_5)()
            solution += current_solution
            problem += '+' + current_problem
    else:
        problem, solution = choice(problems_6)()
        for i in range(6):
            current_problem, current_solution = choice(problems_6)()
            solution += current_solution
            problem += '+' + current_problem
    new_plt((10, 4))
    font = {'family': 'serif', 'fontsize': 24}
    new_score_image(score, '$' + problem + '$', solution, db_sess, font)


@app.route('/addition/<int:_id>', methods=['GET', 'POST'])
@login_required
def addition(_id):
    form = TaskForm()
    info = informations.addition
    template = 'task.html'
    return main_render(form, 'addition', _id, info, template)


@app.route('/subtraction/<int:_id>', methods=['GET', 'POST'])
@login_required
def subtraction(_id):
    form = TaskForm()
    info = informations.subtraction
    template = 'task.html'
    return main_render(form, 'subtraction', _id, info, template)


@app.route('/multiplication/<int:_id>', methods=['GET', 'POST'])
@login_required
def multiplication(_id):
    form = TaskForm()
    info = informations.multiplication
    template = 'task.html'
    return main_render(form, 'multiplication', _id, info, template)


@app.route('/division/<int:_id>', methods=['GET', 'POST'])
@login_required
def division(_id):
    form = TaskForm()
    info = informations.division
    template = 'task.html'
    return main_render(form, 'division', _id, info, template)


@app.route('/complex_arithmetic/<int:_id>', methods=['GET', 'POST'])
@login_required
def complex_arithmetic(_id):
    form = TaskForm()
    info = informations.complex_arithmetic
    template = 'task.html'
    return main_render(form, 'complex_arithmetic', _id, info, template)


@app.route('/complex/<int:_id>', methods=['GET', 'POST'])
@login_required
def complex(_id):
    form = ComplexsForm()
    info = informations.complex
    db_sess = db_session.create_session()
    difficulty = db_sess.query(Difficulty_levels).filter(Difficulty_levels.id == _id).first()
    score = get_score(db_sess, difficulty.difficulty_levels_title, 'complex')

    if form.validate_on_submit():
        if form.new_submit.data:
            score = new_score(score)
            db_sess.add(score)
            db_sess.commit()
            return redirect(f'/complex/{_id}')
        if form.submit.data:
            if form.x.data and form.y.data:
                x1_check, x2_check = score.level_answer.split(';')
                if form.x.data == x1_check and form.y.data == x2_check:
                    score = new_score(score)
                    score.level_rate += 1
                    db_sess.commit()
                    db_sess.add(score)
                    return redirect(f'/complex/{_id}')
                return render_template(
                    'equations.html', form=form, info=info, primer=score.level_url_image,
                    error='Неправильно', title_card=difficulty.difficulty_levels_title,
                    date=score.level_last_date
                )
            return render_template(
                'equations.html', form=form,
                primer=score.level_url_image, info=info,
                error='Заполните данные', title_card=difficulty.difficulty_levels_title,
                date=score.level_last_date
            )
    if not score.level_url_image:
        problem, solution = generators.complex_quadratic()
        new_plt((4, 2))
        font = {'family': 'serif'}
        new_score_image(score, problem, solution, db_sess, font)
    return render_template(
        'equations.html', primer=score.level_url_image, form=form, info=info,
        title=difficulty.difficulty_levels_title, title_card=difficulty.difficulty_levels_title,
        date=score.level_last_date
    )


@app.route('/equations/<int:_id>', methods=['GET', 'POST'])
@login_required
def equations(_id):
    form = EquationsForm()
    info = informations.equations
    db_sess = db_session.create_session()
    difficulty = db_sess.query(Difficulty_levels).filter(Difficulty_levels.id == _id).first()
    score = get_score(db_sess, difficulty.difficulty_levels_title, 'equations')
    if form.validate_on_submit():
        if form.new_submit.data:
            score = new_score(score)
            db_sess.add(score)
            db_sess.commit()
            return redirect(f'/equations/{_id}')
        if form.submit.data:
            if form.x.data and form.y.data:
                x_check, y_check = score.level_answer.split(';')
                if form.x.data == x_check and form.y.data == y_check:
                    score = new_score(score)
                    score.level_rate += 1
                    db_sess.commit()
                    db_sess.add(score)
                    return redirect(f'/equations/{_id}')
                return render_template(
                    'equations.html', form=form,
                    primer=score.level_url_image, info=info,
                    error='Неправильно', title_card=difficulty.difficulty_levels_title,
                                   date=score.level_last_date
                )
            return render_template(
                'equations.html', form=form,
                primer=score.level_url_image, info=info,
                error='Заполните данные', title_card=difficulty.difficulty_levels_title,
                                   date=score.level_last_date
            )
    if not score.level_url_image:
        problem, solution = generators.system_of_equations()
        new_plt((12, 2))
        font = {'family': 'serif', 'fontsize': 24}
        new_score_image(score, problem, solution, db_sess, font)
    return render_template(
        'equations.html', form=form, primer=score.level_url_image,
        title=difficulty.difficulty_levels_title, info=info, title_card=difficulty.difficulty_levels_title,
                                   date=score.level_last_date
    )


@app.route('/basic_algebra/<int:_id>', methods=['GET', 'POST'])
@login_required
def basic_algebra(_id):
    form = TaskForm()
    info = informations.basic_algebra
    template = 'task.html'
    return main_render(form, 'basic_algebra', _id, info, template)


def main():
    db_session.global_init("db/blogs.db")
    app.run(host='0.0.0.0', port=5000)


if __name__ == '__main__':
    main()
