#app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import psycopg2 #pip install psycopg2 
import psycopg2.extras
 
application = Flask(__name__)
application.secret_key = 'okteto'
 
conn=psycopg2.connect(dbname='Scheduling', user='okteto', host='10.152.137.106', password='okteto', port='5432')
conn.autocommit=True
cur=conn.cursor() 

 
@application.route('/')
def Index():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    s = "SELECT * FROM candidate"
    cur.execute(s) # Execute the SQL
    list_candidate = cur.fetchall()
    return render_template('index.html', list_candidate = list_candidate)
 
@application.route('/add_candidate', methods=['POST'])
def add_candidate():
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    if request.method == 'POST':
        fname = request.form['fname']
        job = request.form['job']
        email = request.form['email']
        date = request.form['date']
        company = request.form['company']
        cur.execute("INSERT INTO candidate (fname, job, email, date, company) VALUES (%s,%s,%s,%s,%s)", (fname, job, email, date, company))
        conn.commit()
        flash('Candidate Added successfully')
        return redirect(url_for('Index'))
 
@application.route('/edit/<id>', methods = ['POST', 'GET'])
def get_employee(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('SELECT * FROM candidate WHERE id = %s', (id))
    data = cur.fetchall()
    cur.close()
    print(data[0])
    return render_template('edit.html', candidate = data[0])
 
@application.route('/update/<id>', methods=['POST'])
def update_candidate(id):
    if request.method == 'POST':
        fname = request.form['fname']
        job = request.form['job']
        email = request.form['email']
        date = request.form['date']
        company = request.form['company']
                 
        cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        cur.execute("""
            UPDATE candidate
            SET fname = %s,
                job = %s,
                email = %s,
                date = %s,
                company = %s
            WHERE id = %s
        """, (fname, job, company, email, date,  id))
        flash('Candidate Updated Successfully')
        conn.commit()
        return redirect(url_for('Index'))
 
@application.route('/delete/<string:id>', methods = ['POST','GET'])
def delete_candidate(id):
    cur = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
   
    cur.execute('DELETE FROM candidate WHERE id = {0}'.format(id))
    conn.commit()
    flash('Candidate Removed Successfully')
    return redirect(url_for('Index'))
 
if __name__ == "__main__":
    application.run(debug=True)
