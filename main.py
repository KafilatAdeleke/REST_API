from flask import Flask
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class StudentModel(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.String(100), nullable=False)
	major = db.Column(db.String(100), nullable=False)
	gpa = db.Column(db.Integer, nullable=False)

	def __repr__(self):
		return f"Student(name = {name}, major = {major}, Gpa = {gpa})"

student_put_args = reqparse.RequestParser()
student_put_args.add_argument("name", type=str, help="Name of the Student is required", required=True)
student_put_args.add_argument("major", type=str, help="The Major of the Student", required=True)
student_put_args.add_argument("gpa", type=int, help="Student's Gpa", required=True)

student_update_args = reqparse.RequestParser()
student_update_args.add_argument("name", type=str, help="Name of the Student is required")
student_update_args.add_argument("major", type=str, help="The Major of the Student")
student_update_args.add_argument("gpa", type=int, help="Student's Gpa")

resource_fields = {
	'id': fields.Integer,
	'name': fields.String,
	'major': fields.String,
	'gpa': fields.Integer
}

class Student(Resource):
	@marshal_with(resource_fields)
	def get(self, student_id):
		result = StudentModel.query.filter_by(id=student_id).first()
		if not result:
			abort(404, message="Could not find Student with that id")
		return result

	@marshal_with(resource_fields)
	def put(self, student_id):
		args = student_put_args.parse_args()
		result = StudentModel.query.filter_by(id=student_id).first()
		if result:
			abort(409, message="Student id taken...")

		student = StudentModel(id=student_id, name=args['name'], major=args['major'], gpa=args['gpa'])
		db.session.add(student)
		db.session.commit()
		return student, 201

	@marshal_with(resource_fields)
	def patch(self, student_id):
		args = student_update_args.parse_args()
		result = StudentModel.query.filter_by(id=student_id).first()
		if not result:
			abort(404, message="Student doesn't exist, cannot update")

		if args['name']:
			result.name = args['name']
		if args['major']:
			result.major = args['major']
		if args['gpa']:
			result.gpa = args['gpa']

		db.session.commit()

		return result


	def delete(self, student_id):
		abort_if_student_id_doesnt_exist(student_id)
		del student[student_id]
		return '', 204


api.add_resource(Student, "/student/<int:student_id>")

if __name__ == "__main__":
	app.run(debug=True)
