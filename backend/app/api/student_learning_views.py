from . import student_learning

@student_learning.route('/grades', methods=['GET'])
def get_grades():
    return "Grades"
