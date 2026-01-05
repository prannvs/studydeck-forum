import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'studydeck.settings')
django.setup()

from forum.models import Course, Resource

def populate():
    print("Populating database...")

    courses_data = [
        {"code": "CS F111", "title": "Computer Programming", "dept": "Computer Science"},
        {"code": "MATH F111", "title": "Mathematics I", "dept": "Mathematics"},
        {"code": "EEE F111", "title": "Electrical Sciences", "dept": "EEE"},
    ]

    resources_data = [
        {"course_code": "CS F111", "title": "CP Handout", "type": "PDF", "link": "https://example.com/cp-handout.pdf"},
        {"course_code": "CS F111", "title": "Lecture 1: Variables", "type": "VIDEO", "link": "https://youtu.be/example"},
        {"course_code": "MATH F111", "title": "Calculus Notes", "type": "PDF", "link": "https://example.com/calc.pdf"},
    ]

    for entry in courses_data:
        course, created = Course.objects.get_or_create(
            code=entry["code"],
            defaults={"title": entry["title"], "department": entry["dept"]}
        )
        if created:
            print(f"Created Course: {course.code}")
        else:
            print(f"Course already exists: {course.code}")

    for entry in resources_data:
        try:
            course_obj = Course.objects.get(code=entry["course_code"])
            resource, created = Resource.objects.get_or_create(
                course=course_obj,
                title=entry["title"],
                defaults={"resource_type": entry["type"], "link": entry["link"]}
            )
            if created:
                print(f"Created Resource: {resource.title}")
        except Course.DoesNotExist:
            print(f"Error: Course {entry['course_code']} not found for resource {entry['title']}")

if __name__ == '__main__':
    populate()
    print("Done!")