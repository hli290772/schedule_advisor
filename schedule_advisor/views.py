from django.shortcuts import render, redirect
from .models import *
from datetime import datetime
def index(request):
    return render(request, "schedule_advisor/index.html")
def login(request):
    return render(request, "accounts/login.html")

def signup(request):
    return render(request, "accounts/signup.html")

def browse(request):
    if not request.user.is_authenticated:
        return redirect("..")

    # if add course to schedule
    if request.method == "POST" and request.POST.get('class_nbr'):
        class_nbr = request.POST.get('class_nbr')
        course = Course.objects.filter(class_nbr=class_nbr)[0]
        try:
            course_units = int(course.units)
        except ValueError:
            course_units = 1
        # 15 unit maximum
        if (schedule_units(request.user.profile.courses.all()) + course_units <= 15):
            # No duplicate course
            if (duplicate_courses(request.user.profile.courses.all(), course) == False):
                # No time conflict
                if(can_add_course(request.user.profile.courses.all(), course) == True):
                    # If seats are available
                    if (int(course.enrollment_available) > 0):
                        request.user.profile.courses.add(course)
                    # If waitlist seats are available
                    elif (int(course.wait_tot) > 0):
                        request.user.profile.courses.add(course)
                        message = "There are currently no open seats in this course but there is an open seat on the waitlist so it has been added to your schedule."
                        context = {"subjects": Subject.objects.all(), "message": message}
                        return render(request, "schedule_advisor/browse.html", context)
                    # All seats on waitlist are full
                    else:
                        message = "This course can not be added to your schedule because there are no open seats and the waitlist is full."
                        context = {"subjects": Subject.objects.all(), "message": message}
                        return render(request, "schedule_advisor/browse.html", context)
                else:
                    message = "This course can not be added to your schedule because it has a time conflict with another course in your schedule."
                    context = {"subjects": Subject.objects.all(), "message": message}
                    return render(request, "schedule_advisor/browse.html", context)
            else:
                message = "This course can not be added to your schedule as you already have this course in your schedule."
                context = {"subjects": Subject.objects.all(), "message": message}
                return render(request, "schedule_advisor/browse.html", context)
        else:
            message = "This course can not be added to your schedule as it will exceed the 15 unit maximum. Contact your Dean to discuss options if you wish to take more than 15 units."
            context = {"subjects": Subject.objects.all(), "message": message}
            return render(request, "schedule_advisor/browse.html", context)
        message = "Course addded to your schedule succesfully!"
        context = {"subjects": Subject.objects.all(), "message" : message}
        return render(request, "schedule_advisor/browse.html", context)

    # if search
    if request.method == "POST":
        subject = request.POST.get('subject_search', None)
        catalog_nbr = request.POST.get('catalog_nbr_search', None)
        descr = request.POST.get('descr_search', None)
        courses = Course.objects.all()
        if subject:
            courses = courses.filter(subject=subject)
        if catalog_nbr:
            courses = courses.filter(catalog_nbr=catalog_nbr)
        if descr:
            courses = courses.filter(descr=descr)
        if len(courses) == 0:
            invalidCourseSearchedMessage = "Could not find course; please search for an existing course"
            context = {"subjects": Subject.objects.all(), "invalidCourseSearchedMessage": invalidCourseSearchedMessage}
            return render(request, "schedule_advisor/browse.html", context)

        courses_grouped = {}
        for course in courses:
            group = course.subject + course.catalog_nbr # CS3240
            courses_grouped[group] = courses.filter(subject=course.subject, catalog_nbr=course.catalog_nbr)
        context = {"subjects" : Subject.objects.all(), "courses_grouped" : courses_grouped}
        return render(request, "schedule_advisor/browse.html", context)
    else:
        context = {"subjects": Subject.objects.all()}
        return render(request, "schedule_advisor/browse.html", context)

# can_add_course calculates to see if there is a time conflict between the new_course and other courses in the schedule
def can_add_course(course_list, new_course):
    if not course_list:
        return True
    else:
        for course in course_list:
            if new_course.meetings_days == course.meetings_days:
                new_start_time = datetime.strptime(new_course.meetings_start_time, '%H.%M.%S.%f-05:00').time()
                new_end_time = datetime.strptime(new_course.meetings_end_time, '%H.%M.%S.%f-05:00').time()
                existing_start_time = datetime.strptime(course.meetings_start_time, '%H.%M.%S.%f-05:00').time()
                existing_end_time = datetime.strptime(course.meetings_end_time, '%H.%M.%S.%f-05:00').time()
                if ((new_start_time >= existing_start_time and new_start_time < existing_end_time) or (new_end_time > existing_start_time and new_end_time <= existing_end_time)):
                    return False
        return True

# duplicate_courses checks to see if the course is already in the schedule
def duplicate_courses(course_list, new_course):
    if not course_list:
        return False
    else:
        for course in course_list:
            if (course.subject == new_course.subject) and (course.catalog_nbr == new_course.catalog_nbr):
                return True
        return False

# schedule_units calculates how many units the schedule is
def schedule_units(course_list):
    total_units = 0
    if not course_list:
        total_units += 0
    else:
        for course in course_list:
            try:
                total_units += int(course.units)
            except ValueError:
                total_units += 1
    return total_units

def schedule (request):
    if not request.user.is_authenticated:
        return redirect("..")
    if request.method == 'POST' and request.POST.get('class_nbr'):
        class_nbr = request.POST.get('class_nbr')
        course = Course.objects.filter(class_nbr=class_nbr)[0]
        request.user.profile.courses.remove(course)
    context = {"courses": request.user.profile.courses.all()}
    return render(request, 'schedule_advisor/schedule.html', context)

def advisor(request):
    if not request.user.is_authenticated:
        return redirect("..")
    
    if request.method == "POST" and request.POST.get('advisor'):
        request.user.profile.is_advisor = True
        request.user.profile.save()

    if request.method == "POST" and request.POST.get('student'):
        request.user.profile.is_advisor = False
        request.user.profile.save()

    if request.method == "POST" and request.POST.get('approve'):
        advisee = request.user.advisee.filter(user = User.objects.filter(username=request.POST.get('approve'))[0])[0]
        advisee.approved = True
        advisee.save()

    context = {"is_advisor" : request.user.profile.is_advisor,
               "advisor" : request.user.profile.advisor,
               "advisees" : request.user.advisee.all(),
               "approved" : request.user.profile.approved}
    return render(request, 'schedule_advisor/advisor.html', context)
