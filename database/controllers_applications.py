import datetime

from database.models import Application, ApplicationStep, Contact


from sqlalchemy import *
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///database\\database.db')
Session = sessionmaker(bind=engine)
session = Session()


class ApplicationHelper:
    @staticmethod
    def get_all(status):
        if status == 'declined':
            q = session.query(Application) \
                .filter(Application.decline_date != None)
        elif status == 'applied_only':
            q = session.query(Application) \
                .outerjoin(ApplicationStep) \
                .filter(ApplicationStep.id == None) \
                .filter(Application.decline_date == None)
        elif status == 'running':
            q = session.query(Application) \
                .join(ApplicationStep) \
                .filter(Application.decline_date == None)
        else:
            q = session.query(Application)

        q = q.order_by(Application.application_date.desc())
        applications = q.all()

        return applications

    @staticmethod
    def get(application_id):
        a = session.query(Application).get(application_id)

        return a

    @staticmethod
    def create(**kwargs):
        a = Application(
            created_at_utc=datetime.datetime.utcnow(),
            **kwargs
        )

        session.add(a)
        session.commit()

    @staticmethod
    def update(application_id, **kwargs):
        # ---
        session.query(Application).filter(Application.id == application_id).update(dict(kwargs))
        session.commit()
        session.flush()

    @staticmethod
    def delete(application_id):
        session.query(Application).filter(Application.id == application_id).delete()
        session.commit()
        session.flush()

    @staticmethod
    def get_total(from_, to_):
        q = session.query(Application)

        if from_:
            q = q.filter(Application.application_date >= from_)
        if to_:
            q = q.filter(Application.application_date <= to_)

        applications_total = q.count()

        return applications_total

    @staticmethod
    def get_all_at_least_a_step(from_, to_):
        q = session.query(Application) \
            .join(ApplicationStep) \
            .order_by(ApplicationStep.scheduled_date.asc())

        if from_:
            q = q.filter(ApplicationStep.scheduled_date >= from_)
        if to_:
            q = q.filter(ApplicationStep.scheduled_date <= to_)

        applications = q.all()

        return applications

    @staticmethod
    def get_total_no_step(from_=None, to_=None):
        q = session.query(Application) \
            .outerjoin(ApplicationStep) \
            .filter(ApplicationStep.id == None)

        if from_:
            q = q.filter(Application.application_date >= from_)
        if to_:
            q = q.filter(Application.application_date <= to_)

        applications = q.count()

        return applications

    @staticmethod
    def get_all_declined(from_, to_):
        q = session.query(Application) \
            .filter(Application.decline_date != None)

        if from_:
            q = q.filter(Application.decline_date >= from_)
        if to_:
            q = q.filter(Application.decline_date <= to_)

        applications = q.all()

        return applications

    @staticmethod
    def get_total_by_decline_date(from_, to_):
        q = session.query(Application.decline_date, func.count(Application.decline_date)) \
            .filter(Application.decline_date != None) \
            .group_by(Application.decline_date)

        if from_:
            q = q.filter(Application.decline_date >= from_)
        if to_:
            q = q.filter(Application.decline_date <= to_)

        applications = q.all()

        return applications

    @staticmethod
    def get_total_by_application_date(from_, to_):
        q = session.query(Application.application_date, func.count(Application.application_date)) \
            .group_by(Application.application_date)

        if from_:
            q = q.filter(Application.application_date >= from_)
        if to_:
            q = q.filter(Application.application_date <= to_)

        applications = q.all()

        return applications

    @staticmethod
    def get_min_application_date():
        min_application_date = session.query(func.min(Application.application_date)) \
            .first()[0]

        return min_application_date


class ApplicationStepHelper:
    @staticmethod
    def create(application_id, **kwargs):
        a = ApplicationStep(
            application_id=application_id,
            created_at_utc=datetime.datetime.utcnow(),
            **kwargs
        )

        session.add(a)
        session.commit()

    @staticmethod
    def get(step_id):
        step = session.query(ApplicationStep).get(step_id)

        return step

    @staticmethod
    def update(step_id, **kwargs):
        session.query(ApplicationStep).filter(ApplicationStep.id == step_id).update(dict(kwargs))
        session.commit()
        session.flush()

    @staticmethod
    def delete(step_id):
        session.query(ApplicationStep).filter(ApplicationStep.id == step_id).delete()
        session.commit()
        session.flush()

    @staticmethod
    def get_total(from_, to_):
        q = session.query(ApplicationStep)

        if from_:
            q = q.filter(ApplicationStep.scheduled_date >= from_)
        if to_:
            q = q.filter(ApplicationStep.scheduled_date <= to_)

        steps_total = q.count()

        return steps_total

    @staticmethod
    def get_all(from_, to_, sort_by=None):
        q = session.query(ApplicationStep) \
            .order_by(ApplicationStep.application_id, ApplicationStep.scheduled_date.asc())

        if from_:
            q = q.filter(ApplicationStep.scheduled_date >= from_)
        if to_:
            q = q.filter(ApplicationStep.scheduled_date <= to_)

        if sort_by and sort_by == 'application_id':
            q = q.order_by(ApplicationStep.application_id)

        applications = q.all()

        return applications

    @staticmethod
    def get_total_by_scheduled_date(from_, to_):
        q = session.query(ApplicationStep.scheduled_date, func.count(ApplicationStep.scheduled_date)) \
            .group_by(ApplicationStep.scheduled_date)

        if from_:
            q = q.filter(ApplicationStep.scheduled_date >= from_)
        if to_:
            q = q.filter(ApplicationStep.scheduled_date <= to_)

        steps = q.all()

        return steps


class ContactHelper:
    @staticmethod
    def create(application_id, **kwargs):
        a = Contact(
            application_id=application_id,
            **kwargs
        )

        session.add(a)
        session.commit()

    @staticmethod
    def get(contact_id):
        contact = session.query(Contact).get(contact_id)

        return contact

    @staticmethod
    def update(contact_id, **kwargs):
        session.query(Contact).filter(Contact.id == contact_id).update(dict(kwargs))
        session.commit()
        session.flush()

    @staticmethod
    def delete(contact_id):
        session.query(Contact).filter(Contact.id == contact_id).delete()
        session.commit()
        session.flush()


if __name__ == '__main__':
    from sqlalchemy import *
    from sqlalchemy.orm import sessionmaker
    from faker import Faker

    engine = create_engine('sqlite:///database.db')
    Session = sessionmaker(bind=engine)
    session = Session()

    APPLICATIONS = 10
    STEPS_RANGE = (0, 3)
    CONTACTS_RANGE = (0, 3)

    fake = Faker('fr_FR')

    today = datetime.date.today()

    for a in range(APPLICATIONS):
        application_id = a + 1

        start_date = today - datetime.timedelta(days=30)
        application_date = fake.date_between(start_date=start_date, end_date=today)

        decline_date = None
        is_declined = fake.boolean(chance_of_getting_true=30)
        if is_declined:
            end_date = min(application_date + datetime.timedelta(days=30), today)
            decline_date = fake.date_between(start_date=application_date, end_date=end_date)

        application = {
            'job_title': fake.job(),
            'company': fake.company(),
            'city': fake.city(),
            'application_date': application_date,
            'decline_date': decline_date,
            'via': fake.random_choices(elements=('linkedin', 'website'))[0],
            'offer_link': 'https://example.com/',
            'notes': fake.text(max_nb_chars=50),
            'map_link': 'https://maps.google.com/',
        }
        ApplicationHelper.create(**application)

        has_steps = fake.boolean(chance_of_getting_true=70)
        if has_steps:
            nb_steps = fake.pyint(min_value=STEPS_RANGE[0], max_value=STEPS_RANGE[1])
            min_date = application_date + datetime.timedelta(days=1)
            for s in range(nb_steps):
                end_date = min_date + datetime.timedelta(days=10)
                scheduled_date = fake.date_between(start_date=min_date, end_date=end_date)

                step = {
                    'name': fake.random_choices(elements=('HR interview', 'CEO interview', 'CTO interview', 'CFO interview'))[0],
                    'scheduled_date': scheduled_date,
                    'via': fake.random_choices(elements=('On-site', 'Video call', 'Phone call', 'At home', 'Other'))[0],
                    'notes': fake.text(max_nb_chars=50),
                }
                ApplicationStepHelper.create(application_id=application_id, **step)

                min_date = scheduled_date

        has_contacts = fake.boolean(chance_of_getting_true=70)
        if has_contacts:
            nb_contacts = fake.pyint(min_value=CONTACTS_RANGE[0], max_value=CONTACTS_RANGE[1])
            for c in range(nb_contacts):
                contact = {
                    'name': fake.name(),
                    'position': fake.random_choices(elements=('CEO', 'CTO', 'CFO', 'HR', 'Recruiter'))[0],
                    'notes': fake.text(max_nb_chars=50),
                }
                ContactHelper.create(application_id=application_id, **contact)