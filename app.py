from flask import Flask, jsonify, request
from flask_cors import CORS
from os import environ, getcwd, path
from config import db, SECRET_KEY
from dotenv import load_dotenv
from models.user import User
from models.personalDetails import PersonalDetails
from models.projects import Projects
from models.experiences import Experiences
from models.education import Education
from models.certificate import Certificate
from models.skills import Skills


def create_app():
    app=Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"]=environ.get("DB_URI")
    app.config["SQLALCHEMY_TRACL_MODIFICATIONS"]=False
    app.config["SQLALCHEMY_ECHO"]=False
    app.secret_key=SECRET_KEY
    db.init_app(app)
    print("DB initialized successfully")

    with app.app_context():
        #db.drop_all()  #when any change will proceed then use this

        """
        create an end point

        Use form data to take the responcres from the user
        Use username for indexing a user
            -signup user
            -add personal detail
            -add experience details
            -add project details
            -add education details
            -add certificate details
            -add skills details
        """
#FOR SIGNUP USER
        @app.route("/sign_up",methods=['POST'])
        def signup():
            data = request.form.to_dict(flat=True)

            new_user = User(
                username = data["username"]
            )
            db.session.add(new_user)
            db.session.commit()

            return "User added successfully"

#ADD PERSONAL DETAILS
        @app.route("/add_personal_details",methods=['POST'])
        def add_personal_details():
            username = request.args.get('username')
            user = User.query.filter_by(username=username).first()
            """
            {
                "name":"",
                "email":"",
                "phone":"",
                "address":"",
                "linkedlink":""
            }
            """

            personal_details = request.get_json()

            new_personal_details = PersonalDetails(
                name=personal_details["name"],
                email=personal_details["email"],
                phone=personal_details["phone"],
                address=personal_details["address"],
                linkedin_link=personal_details["linkedin_link"],
                user_id=user.id
            )

            db.session.add(new_personal_details)
            db.session.commit()
            return "Personal Details added successfully!!!"

#ADD EXPERIENCE DETAILS
        @app.route("/add_experience_details",methods=['POST'])
        def add_experience_details():
            username = request.args.get('username')
            user  =User.query.filter_by(username=username).first()               
            experience_details = request.get_json()
            print(experience_details)
            for project in experience_details["data"]:
                new_experiences=Experiences(
                    companyname=Experiences["name"],
                    role = Experiences["role"],
                    role_desc=project["role_desc"],
                    start_date=project["start_date"],
                    end_date=project["end_date"],
                    user_id=user.id
                    )
                db.session.add(new_experiences)
                db.session.commit()
                return "Added new experience details successfully!!!"

#ADD PROJECT DETAILS
        @app.route("/add_project_details",methods=['POST'])
        def add_project_details():
            username = request.args.get('username')
            user  =User.query.filter_by(username=username).first()
                
            project_details = request.get_json()

#ADD EDUCATION DETAILS
        @app.route("/add_education_details",methods=['POST'])
        def add_education_details():
            username = request.args.get('username')
            user  =User.query.filter_by(username=username).first()
                
            education_details = request.get_json()

#ADD CERTIFICATE DETAILS
        @app.route("/add_certificate_details",methods=['POST'])
        def add_certificate_details():
            username = request.args.get('username')
            user  =User.query.filter_by(username=username).first()
                
            certificate_details = request.get_json()

#ADD SKILLS DETAILS
        @app.route("/add_skills_details",methods=['POST'])
        def add_skills_details():
            username = request.args.get('username')
            user  =User.query.filter_by(username=username).first()
                
            skills_details = request.get_json()

#ADD PROJECT DETAILS
        @app.route("/add_projects", methods =["POST"])
        def add_projects():
            username=request.args.get("username")
            user = User.query.filter_by(username=username).first()
            project_data = request.get_json()
            print(project_data)
            for project in project_data["data"]:
                new_project=Projects(
                    name=project["name"],
                    desc=project["description"],
                    start_date=project["start_date"],
                    end_date=project["end_date"],
                    user_id=user.id
                    )
                db.session.add(new_project)
                db.session.commit()
                return "Successfully added projectdetails "

        @app.route('/get_resume', methods = ["POST"])
        def get_resume():
            username=request.args.get("username")
            user = User.query.filter_by(username=username).first()
            personal_details = PersonalDetails.query.filter_by(user_id=user.id).first()
            experiences = Experiences.query.filter_by(user_id=user.id).all()
            education = Education.query.filter_by(user_id=user.id).all()
            projects = Projects.query.filtetr_by(user_id=user.id).all()
            certificates = Certificate.query.filter_by(user_id=user.id).all()
            skills = Skills.query.filter_by(user_id=user.id).all()


            experiences_data = []
            education_data = []
            projects_data = []
            certificates_data = []
            skills_data = []

            resume_data = {
                "name": personal_details.name,
                "email": personal_details.email,
                "phone": personal_details.phone,
                "address": personal_details.address,
                "linkedin_link": personal_details.linkedin_link
            }

            #ADD EXPERIENCES
            for exp in experiences:
                experiences_data.append({
                    "company_name": exp.company_name,
                    "role": exp.role,
                    "role_desc": exp.role_desc,
                    "start_date": exp.start_date,
                    "end_date": exp.end_date                
                    })
                resume_data["experiences"] = experiences_data
            #ADD PROJEFCTS
            for proj in projects :
                projects_data.append({
                    "name":proj.name,
                    "desc":proj.desc,
                    "start_date": proj.start_date,
                    "end_date": proj.end_date
                })

            resume_data["projects"] = projects_data
            return resume_data
            
        db.create_all()
        db.session.commit()
        return app

if __name__=="__main__":
    app=create_app()
    app.run(debug=True)