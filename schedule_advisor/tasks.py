from celery import Celery, shared_task
from .models import Subject, Course
import requests

app = Celery('tasks', broker='amqp://localhost')

@shared_task()
def update():
    # get all departments
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearchOptions?institution=UVA01&term=1238"
    r = requests.get(url)
    for subject in r.json()['subjects']:
        _abbreviation = subject['subject']
        _description = subject['descr']
        _subject = Subject(abbreviation=_abbreviation,description=_description)
        _subject.save()

def update2():
    Course.objects.all().delete()

    subjects = Subject.objects.all()
    url = "https://sisuva.admin.virginia.edu/psc/ihprd/UVSS/SA/s/WEBLIB_HCX_CM.H_CLASS_SEARCH.FieldFormula.IScript_ClassSearch?institution=UVA01&term=1238&page="
    
    for subject in subjects:
        empty = False
        page = 1
        while not empty:
            cur_url = url + str(page) + '&subject=' + subject.abbreviation
            r = requests.get(cur_url)
            if (len(r.json()) == 0):
                empty = True
            else:
                for course in r.json():
                    if len(course['meetings']) != 0:
                        _days = course['meetings'][0]['days']
                        _start_time = course['meetings'][0]['start_time']
                        _end_time = course['meetings'][0]['end_time']
                        _facility_descr = course['meetings'][0]['facility_descr']
                    else:
                        _days = '0'
                        _start_time = '0'
                        _end_time = '0'
                        _facility_descr = '0'
                    Course(class_section=course['class_section'],
                           class_nbr=course['class_nbr'],
                           subject=course['subject'],
                           catalog_nbr=course['catalog_nbr'],
                           wait_tot=course['wait_tot'],
                           wait_cap=course['wait_cap'],
                           class_capacity=course['class_capacity'],
                           enrollment_total=course['enrollment_total'],
                           enrollment_available=course['enrollment_available'],
                           descr=course['descr'],
                           units=course['units'],
                           instructor_name=course['instructors'][0]['name'],
                           meetings_days=_days,
                           meetings_start_time=_start_time,
                           meetings_end_time=_end_time,
                           meetings_facility_descr=_facility_descr,
                            ).save()
            page += 1
        print(subject.abbreviation + 'done!')