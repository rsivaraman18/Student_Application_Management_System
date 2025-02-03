from flask import Flask, render_template, request, redirect, url_for, session,flash, send_from_directory
from models import db, Mystudents
from werkzeug.utils import secure_filename
import os
from fpdf import FPDF
from flask_migrate import Migrate 

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'
app.config['UPLOAD_FOLDER'] = 'uploads/'

# Configure the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/studentmanagement'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable modification tracking to save memory

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db) 


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')



@app.route('/construct', methods=['GET', 'POST'])
def construction():
    return render_template('construct.html')





# Route for displaying the student application form
@app.route('/apply', methods=['GET', 'POST'])
def apply():
    if request.method == 'POST':
        
        name = request.form.get('name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        dob = request.form.get('dob')
        gender = request.form.get('gender')

        degree = request.form.get('degree')
        institution_name = request.form.get('institution_name')
        passed_year = request.form.get('passed_year')
        degree_certificate = request.files.get('degree_certificate')
        id_proof = request.files.get('id_proof')

        city = request.form.get('city')
        state = request.form.get('state')
        password = request.form.get('password')
        conpassword = request.form.get('conpassword')



        # Securely save the files
        if degree_certificate:
            degree_certificate_filename = secure_filename(degree_certificate.filename)
            degree_certificate.save(os.path.join(app.config['UPLOAD_FOLDER'], degree_certificate_filename))
        if id_proof:
            id_proof_filename = secure_filename(id_proof.filename)
            id_proof.save(os.path.join(app.config['UPLOAD_FOLDER'], id_proof_filename))

        # Save data into the database
        new_application = Mystudents(
            name=name,
            email=email,
            phone=phone,
            dob=dob,
            gender=gender,
            degree=degree,
            institution_name=institution_name,
            passed_year=passed_year,
            degree_certificate=degree_certificate_filename,
            id_proof=id_proof_filename,
            city=city,
            state=state,
            password=password,
            conpassword=conpassword,
        )

        try:
            db.session.add(new_application)
            db.session.commit()
            flash('Application submitted successfully!', 'success')
            return redirect(url_for('apply'))
        except Exception as e:
            db.session.rollback()
            flash('Error submitting application. Try again later.', 'danger')
            print(e)

    return render_template('apply.html')



# Route for displaying all student applications for the admin
@app.route('/admin', methods=['GET'])
def admin():
    applications = Mystudents.query.all()  # Fetch all applications from the database
    return render_template('admin.html', applications=applications)


# Route for approving a student's application
@app.route('/approve/<int:id>', methods=['GET'])
def approve(id):
    application = Mystudents.query.get(id)
    if application:
        application.status = 'Approved'  # Update application status
        db.session.commit()

        # Generate PDF admission letter
        generate_admission_pdf(application)

        flash('Application approved and admission letter generated!', 'success')
    return redirect(url_for('admin'))

# Route for rejecting a student's application
@app.route('/reject/<int:id>', methods=['GET'])
def reject(id):
    application = Mystudents.query.get(id)
    if application:
        application.status = 'Denied'  # Update application status
        db.session.commit()
        flash('Application rejected!', 'danger')
    return redirect(url_for('admin'))




# # Function to generate PDF admission letter
# def generate_admission_pdf(application):
#     pdf = FPDF()
#     pdf.add_page()
#     pdf.set_font("Arial", size=12)

#     pdf.cell(200, 10, txt="Admission Letter", ln=True, align='C')
#     pdf.ln(10)  # Line break

#     pdf.cell(200, 10, txt=f"Name: {application.name}", ln=True)
#     pdf.cell(200, 10, txt=f"Degree: {application.degree}", ln=True)
#     pdf.cell(200, 10, txt=f"Institution: {application.institution_name}", ln=True)
#     pdf.cell(200, 10, txt=f"Passed Year: {application.passed_year}", ln=True)
#     pdf.cell(200, 10, txt=f"Email: {application.email}", ln=True)

#     pdf_output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'admission_{application.id}.pdf')
#     pdf.output(pdf_output_path)







from fpdf import FPDF
import os
from datetime import datetime

def generate_admission_pdf(application):
    pdf = FPDF()
    pdf.add_page()

    # Set fonts and styles
    pdf.set_font("Arial", 'B', size=16)
    pdf.cell(200, 10, txt="Admission Letter", ln=True, align='C')

    pdf.ln(10)  # Line break

    # Add decorative border
    pdf.rect(10, 10, 190, 277)

    # Add date
    pdf.set_font("Arial", size=12)
    current_date = datetime.now().strftime("%B %d, %Y")
    pdf.cell(200, 10, txt=f"Date: {current_date}", ln=True)

    # Add student details
    pdf.ln(5)  # Line break

    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Name: {application.name}", ln=True)
    pdf.cell(200, 10, txt=f"Degree: {application.degree}", ln=True)
    pdf.cell(200, 10, txt=f"Institution: {application.institution_name}", ln=True)
    pdf.cell(200, 10, txt=f"Passed Year: {application.passed_year}", ln=True)
    pdf.cell(200, 10, txt=f"Email: {application.email}", ln=True)
    pdf.cell(200, 10, txt=f"Phone: {application.phone}", ln=True)
    pdf.cell(200, 10, txt=f"Date of Birth: {application.dob.strftime('%B %d, %Y')}", ln=True)
    pdf.cell(200, 10, txt=f"Gender: {application.gender}", ln=True)
    pdf.cell(200, 10, txt=f"City: {application.city}", ln=True)
    pdf.cell(200, 10, txt=f"State: {application.state}", ln=True)

    pdf.ln(10)  # Line break

    # Add instructions or extra message
    pdf.set_font("Arial", style='I', size=12)
    pdf.multi_cell(0, 10, txt="Congratulations! You have been selected for admission to the program. Please "
                              "follow the next steps outlined in the admission guidelines sent via email.")

    # Add footer or custom notes (if any)
    pdf.set_font("Arial", 'I', size=10)
    pdf.ln(20)  # Line break
    pdf.cell(200, 10, txt="This letter is generated automatically. Please contact the institution for any inquiries.", ln=True, align="C")

    # Save the PDF
    pdf_output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'admission_{application.id}.pdf')
    pdf.output(pdf_output_path)







# Route for downloading the admission letter PDF
@app.route('/download_pdf/<int:id>', methods=['GET'])
def download_pdf(id):
    pdf_filename = f'admission_{id}.pdf'
    return send_from_directory(app.config['UPLOAD_FOLDER'], pdf_filename)





@app.route('/studentlogin', methods=['GET', 'POST'])
def student_login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        if not email or not password:
            flash('Please enter both email and password.', 'warning')
            return redirect(url_for('student_login'))

        # Check if the student exists in the database
        student = Mystudents.query.filter_by(email=email).first()

        if not student:
            flash('No account found with this email.', 'danger')
            return redirect(url_for('student_login'))

        
        if password != student.password:  
            flash('Incorrect password. Please try again.', 'danger')
            return redirect(url_for('student_login'))

        # Store session data after successful login
        session['student_id'] = student.id
        session['email'] = student.email
        flash('Login successful!', 'success')

        return redirect(url_for('student_profile'))  # Redirect to student profile

    return render_template('studentlogin.html')


@app.route('/logout')
def logout():
    session.clear()  # Clear all session data
    flash('You have been logged out.', 'info')
    return redirect(url_for('student_login'))  # Redirect to login page

@app.route('/studentprofile')
def student_profile():
    if 'student_id' not in session:
        flash('Please log in first.', 'warning')
        return redirect(url_for('student_login'))

    student = Mystudents.query.get(session['student_id'])

    if not student:
        flash('Student record not found.', 'danger')
        return redirect(url_for('student_login')) 
    return render_template('studentprofile.html', student=student) 


@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)






# Run the app
if __name__ == '__main__':
    app.run(debug=True)
