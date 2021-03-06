from . import bp
from app.models import User, Deal, TaskCard
from faker import Faker
from datetime import datetime
from random import choice


@bp.route('/', methods=['GET'])
def generate_all_data():
    # TODO: Add check if data already generated!
    fake = Faker()
    # 1. Generate 100 new users and save them to DB and in array
    user_array = []
    for _ in range(100):
        user = User()
        fake_profile = fake.simple_profile()
        user.username = fake_profile['name']
        user.email = fake_profile['mail']
        user.avatar = 'https://api.adorable.io/avatars/150/' + fake_profile['mail']
        user_array.append(user)
        user.save()
    # 2. Generate 500 new tasks and set users from random array. Dates must be prev, current and next month
    current_date = datetime.utcnow()
    for _ in range(500):
        task = TaskCard()
        task.task_due_date = fake.date_between(start_date='-2M', end_date='+2M')
        task.task_type = choice(['Reminder', 'Call', 'Event'])
        if task.task_due_date < current_date:
            task.task_status = choice(['Completed', 'Ended'])
        else:
            task.task_status = choice(['Active', 'Completed'])
        task.task_body = fake.sentence(nb_words=8)
        task.assigned_by_user = choice(user_array)
        task.save()

    # 3. Generate 10000 new deals in period: start date - first day of the year, end date - current date
    for _ in range(10000):
        new_deal = Deal()
        new_deal.deal_date = fake.date_between(start_date=current_date.replace(day=1, month=1),
                                               end_date=current_date.replace(day=31, month=12))
        new_deal.amount = fake.random_int(min=300, max=10000)
        new_deal.client = fake.company()
        new_deal.save()

    return {
        'msg': 'OK'
    }, 201


@bp.route('/', methods=['DELETE'])
def reset_all_data():
    Deal.drop_collection()
    TaskCard.drop_collection()
    User.drop_collection()

    return {'msg': 'OK'}
