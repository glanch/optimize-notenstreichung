from __future__ import print_function
from optlang import Model, Variable, Constraint, Objective
from sympy import Sum

curriculum = [
    {
        "name": "Praktische Informatik",
        "courses": [
            {
                "name": "Programmierung",
                "ects": 8,
                "discardable": True
            },
            {
                "name": "DatenstrukturenundAlgorithmen",
                "ects": 8,
                "discardable": True
            },
            {
                "name": "DatenbankenundInformationssysteme",
                "ects": 6,
                "discardable": True
            },
            {
                "name": "Softwaretechnik",
                "ects": 6,
                "discardable": True
            }
        ]
    },
    {
        "name": "Technische Informatik",
        "courses": [
            {
                "name": "EinführungindieTechnischeInformatik",
                "ects": 6,
                "discardable": True
            },
            {
                "name": "BetriebssystemeundSystemsoftware",
                "ects": 6,
                "discardable": True
            },
            {
                "name": "Datenkommunikation und Sicherheit",
                "ects": 6,
                "discardable": True
            }
        ]
    }
]

grades = {
    "DatenkommunikationundSicherheit": 1.0,
    "MathematischeLogik": 1.0,
    "Programmierung": 3.2,
    "DatenstrukturenundAlgorithmen": 1.6,
    "DatenbankenundInformationssysteme": 3.2,
    "Softwaretechnik": 2.0
}


def optimize_grades(curriculum, grades, max_ects):
    sum_credits = sum(
        course["ects"] for fachbereich in curriculum for course in fachbereich["courses"])
    courses = [
        course for fachbereich in curriculum for course in fachbereich["courses"]]

    total_ects = 0

    # variables whether on grade should be discarded and build up total_ects at the same time
    discard_grade = {}
    for course in courses:
        course_name = course["name"]
        discard_grade[course_name] = Variable(
            f"discard_{course_name}", lb=0, type="binary")
        total_ects += course["ects"]

    # create objective being the sum of all grades that are not
    obj = Objective(sum(
        (grades[course["name"]]*course["ects"] / total_ects)*(1-discard_grade[course["name"]]) for course in courses), direction="min")

    # create constraints
    constraints = []

    # for every fachbereich at most one grade can be discarded
    for fachbereich in curriculum:
        constraints.append(Constraint(
            sum(discard_grade[course["name"]] for course in fachbereich["courses"]), ub=1))

    # at most max_ects can be discarded
    for course in courses:
        constraints.append(Constraint(
            course["ects"]*discard_grade[course["name"]], ub=max_ects))

    # create model
    model = Model(name='Grade Optimizer')
    model.objective = obj

    model.add(constraints)

    status = model.optimize()

    print("status:", model.status)
    print("objective value:", model.objective.value)
    print("----------")
    for var_name, var in model.variables.iteritems():
        print(var_name, "=", var.primal)


def taken_courses(grades, curriculum):
    return [course for fachbereich in curriculum for course in fachbereich["courses"] if course["name"] in grades.keys()]


optimize_grades(curriculum, grades, 6)
