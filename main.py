# imports
from cgi import test
import csv
import marshal
import sys
import json

from data import DataSet


def writeToJSON(filename, courses, students, tests, marks):

    # bool flag for incomplete course weight
    isError = False
    report_error = {"error": "Invalid course weights"}

    report_summary = {"student": list()}

    for student in students:

        student_name = student["name"]
        student_id = student["id"]

        # calculate student average
        student_average = 0
        course_averages = []

        # get the marks for this student
        student_marks = [item for item in marks if item["student_id"] == student_id]

        # get the tests taken by this student
        tests_taken = [
            item for item in tests for m in student_marks if item["id"] == m["test_id"]
        ]

        for c in courses:
            course_average = 0

            course_weights = [
                item for item in tests_taken if c["id"] == item["course_id"]
            ]

            course_marks = [
                item
                for item in student_marks
                for weights in course_weights
                if item["test_id"] == weights["id"]
            ]

            for x in range(len(course_marks)):
                course_average += (
                    float(course_marks[x]["mark"])
                    * float(course_weights[x]["weight"])
                    / 100
                )

            if course_average != 0:
                course_averages.append(
                    {
                        "id": int("{}".format(c["id"])),
                        "name": "{}".format(c["name"]).strip(),
                        "teacher": "{}".format(c["teacher"]).strip(),
                        "courseAverage": round(course_average, 2),
                    }
                )

        for course_detail in course_averages:
            student_average += course_detail["courseAverage"]

        student_average /= len(course_averages)

        student_summary = {
            "id": student_id,
            "name": student_name,
            "totalAverage": round(student_average, 2),
            "courses": course_averages,
        }

        report_summary["student"].append(student_summary)

    if isError:
        json_data = json.dumps(report_error, indent=2)
    else:
        json_data = json.dumps(report_summary, indent=2)

    with open(filename, "w") as jsonfile:
        jsonfile.write(json_data)


# main function
def main(args):

    # read files
    course_data = DataSet(args[1]).data
    students_data = DataSet(args[2]).data
    test_data = DataSet(args[3]).data
    marks_data = DataSet(args[4]).data

    writeToJSON(args[5], course_data, students_data, test_data, marks_data)



if __name__ == "__main__":

    main(sys.argv)
