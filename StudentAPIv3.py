from flask import Flask
from flask_restx import Api, Resource, fields

app = Flask(__name__)
api = Api(app, version='1.0', title='Student_Management_Owner_Portal API',
    description='Student_Management',
)

ns = api.namespace('Students', description='Students Management Operations')


student = api.model('Student',             
    {
        'student_id': fields.Integer(readonly=True, description='The task unique identifier'),
        'name': fields.String(required=True, description='The task details'),
        'age': fields.String(required=True, description='The task details'),
        'spec': fields.String(required=True, description='The task details')
    }
)


class StudentDOA(object):
    def __init__(self):
        self.counter = 0
        self.students = []

    def get(self, student_id):
        for student in self.students:
            if student['student_id'] == student_id:
                return student
        api.abort(404, "Student {} doesn't exist".format(student_id))

    def create(self, data):
        student = data
        student['student_id'] = self.counter = self.counter + 1
        self.students.append(student)
        return student
    
    def update(self, student_id, data):
        student = self.get(student_id)
        student.update(data)
        return student
    
    def delete(self, student_id):
        student = self.get(student_id)
        self.students.remove(student)

DAO = StudentDOA()
DAO.create({"name": "Mark","age": 23,"spec": "math"}),
DAO.create({"name": "Jane","age": 20,"spec": "biology"}),
DAO.create({"name": "Peter","age": 21,"spec": "history"}),
DAO.create({"name": "Kate","age": 22,"spec": "science"})

#DAO.create({'task': '?????'})
#DAO.create({'task': 'profit!'})


@ns.route('/')
class StudentsList(Resource):
    '''Shows a list of all Students, and lets you POST to add new tasks'''
    @ns.doc('list_Students')
    @ns.marshal_list_with(student)
    def get(self):
        '''List all tasks'''
        return DAO.students
    
    @ns.doc('create_student')
    @ns.expect(student)
    @ns.marshal_with(student, code=201)
    def post(self):
        '''Create a new students'''
        return DAO.create(api.payload), 201


@ns.route('/<int:id>')
@ns.response(404, 'student not found')
@ns.param('id', 'The task identifier')
class Student(Resource):
    '''Show a single student item and lets you delete them'''
    @ns.doc('get_student')
    @ns.marshal_with(student)
    def get(self, id):
        '''Fetch a given resource'''
        return DAO.get(id)
    
    @ns.doc('delete_student')
    @ns.response(204, 'student deleted')
    def delete(self, id):
        '''Delete a student given its identifier'''
        DAO.delete(id)
        return DAO.get(id), 204
    
    @ns.expect(student)
    @ns.marshal_with(student)
    def put(self, id):
        '''Update a student given its identifier'''
        return DAO.update(id, api.payload)
    
if __name__ == '__main__':
    app.run(debug=True)