from flask import Flask, render_template, jsonify, request, flash
from flask_hcaptcha import hCaptcha
import os
#from database import engine
#from sqlalchemy import text
from database import load_jobs_from_db, load_job_from_db, add_application_to_db
#An App is an object of Flask class. It is our WSGI application. WSGI stands for Web Server Gateway Interface.
#In any python script, you have this variable __name__ which is a built-in variable.
"""this variable refers to how a particular script was invoked. In this case the script was invoked as the main script. That's why __main__ is the value of __name__ variable."""

app = Flask(__name__)
hcaptcha = hCaptcha(app)
SECRET_HCAPTCHA = os.environ['SECRET_HCAPTCHA']
SITE_KEY_HCAPTCHA = os.environ['SITE_KEY_HCAPTCHA']
app.config.update({
    "debug": True,
    "HCAPTCHA_SITE_KEY": "SITE_KEY_HCAPTCHA",
    "HCAPTCHA_SITE_SECRET": "SECRET_HCAPTCHA",
    "HCAPTCHA_ENABLED": True
})

"""The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function. In this case, the URL of the given function (hello_world) is '/'.
We tell Flask when a certain URL is requested, the function is called and the return value of the function is sent to the browser as a response. In this case we registering a route, which is simply a part of the URL after the domain name. For example, if you go to www.example.com/hello, the path of the route is /hello.
And the domain name is www.example.com.

The symbol '@' is a decorator. A decorator is a design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure. Decorators are usually called before the definition of a function you want to decorate."""

"""It is not a good practice to list all the jobs in the HTML file. Instead, we should list them in the python file and then pass them to the HTML file. And then is sent to the browser as a response we can see on the screen.
So we simulated a database with a list of dictionaries. Each dictionary represents a job. And then we pass this list to the HTML file. And then we can use this list in the HTML file, using Flask templating syntax.
"""
"""Another way to return dynamic data - besides Flask templating syntax - is to use the jsonify function. This function converts a dictionary into a JSON object. JSON stands for JavaScript Object Notation. It is a lightweight data-interchange format. It is easy for humans to read and write and easy for machines to parse and generate.
The JSON format usage is strictly linked to the concept of RESTful APIs. REST stands for Representational State Transfer. It is an architectural style for designing networked applications. It relies on a stateless, client-server, cacheable communications protocol -- the HTTP. 
RESTful means that the API follows the REST principles.
The difference between REST API and RESTful API is that REST API is a set of rules and principles that define how a client and server should communicate, while RESTful API is an API that follows these rules and principles.
RESTful APIs are used to exchange data between a client and a server. The client sends a request to the server and the server sends a response back to the client. The response is usually in the form of a JSON object. So instead of returning HTML, we can return JSON. And then the client can use this JSON to display the data in the browser. 

With the function list_jobs, we used jsonify to return a JSON object. The jsonify function converts a dictionary into a JSON object. The dictionary is the list of jobs. The list of jobs is a list of dictionaries. Each dictionary represents a job. We registered a new route /jobs, in which we return the list of jobs as a JSON object. When people say rest API or JSON API, or API endpoint, they are talking about a URL that returns data in the form of a JSON object.

So the difference between creating an HTML endpoint and a JSON endpoint is that the HTML endpoint returns HTML and the JSON endpoint returns JSON. The HTML endpoint is used to display data in the browser and the JSON endpoint is used to exchange data between a client and a server.

In order to differentiate between the two, often a route starting with /api is used for JSON endpoints. For example, /api/jobs. This is a convention. It is not a rule. So we can use /jobs for HTML endpoints and /api/jobs for JSON

API stands for Application Programming Interface. It is a set of rules and protocols that allows different software applications to communicate with each other. ABI stands for Application Binary Interface. The difference between API and ABI is that API is a set of rules and protocols that allows different software applications to communicate with each other, while ABI is a set of rules and protocols that allows different software applications to communicate with each other at the binary level.

In this context, microservices are small, independent services that communicate with each other using APIs. They are small, independent services that can be developed, deployed, and scaled independently. They are not monolithic applications. Monolithic applications are large, single applications that do everything.

We also imported text from sqlalchemy to be able to use the text function to execute raw SQL queries. engine.connet() is used to create a connection to the database. The connection is used to execute SQL queries. The connection is closed after the queries are executed.

We imported engine from database.py to be able to use the engine object to create a connection to the database. We used the text function to execute raw SQL queries. This is another syntax to import .py files, it is called relative import. It is used to import modules from the same package. In this case, we are importing engine from database.py. 

So we used the engine to create a "result" object which is a CursorResult object, from which we obtain the "rows" object wich is basically a list of RowMapping objects, and then we convert it to "jobs" object, which is a list of dictionaries. 

We replaced the JSON object JOBS with the database object jobs,which is a list of dictionaries, JOBS was an hardcoded
list of dictionaries, while jobs is a list of dictionaries obtained in a dynamic way, from a cloud-based database.

The helper function load_jobs_from_db() is used to load the jobs from the database. But we moved it to database.py, so that routes and helper functions are separated. The app.py file is only used to define routes. The database.py file is used to define helper functions.

With the line "from database import load_jobs_from_db" is like we are proxy importing text from sqlalchemy and engine from database.py, so we can use them in app.py, because both are used in load_jobs_from_db() function. This is good encapsulation, and good coding practice. All your database-related logic should be in database.py, and all your route-related logic should be in app.py.

We also changed the route /jobs to /api/jobs, so that it is clear that it is a JSON endpoint.

We added a new route /jobs/<id> to return a single job. The <id> is a placeholder for the job id. The job id is a unique identifier for a job. It is a string. It is not an integer. <id> can change dynamically, so it is a placeholder. It is a variable. It is a path parameter. It is a part of the URL/route. In this new route we also added an if statement to check if the job exists. If the job does not exist, we return a 404 error. If the job exists, we return the job. In reality, there are no differences in the aspect of the page, between "return "Not Found", 404" and simply "return "Not Found"".

We also had to add a new helper function load_job_from_db(id) in database.py to load a single job from the database. The function takes an id as an argument and returns a single job. The function uses the text function to execute raw SQL queries. The function uses the engine object to create a connection to the database. The function uses the connection to execute SQL queries.

We adden a new route /job/<id>/apply to apply to a job. When we compile a form and submit it, a full address in the browser is generated, with the action as the first part of the address, and the input as the second part of the address, separated by a question mark. We need to parse the address in the route, and extract the input from it. In order to do that, we import request from flask. The request object contains all the data sent from the browser to the server. The request object is a dictionary. The request object contains all the data sent from the browser to the server.

This route is used to apply to a job. When we apply to a job, we send a POST request to the server, by using the option "methods=['post']". The POST request contains all the data sent from the browser to the server. In this way the data is "posted" by the browser instead of being sent to the URL.

We indeed changed "data" from request.args to request.form, because request.args is used to get data from the URL, while request.form is used to get data from the form. The form is obtained with the POST method.

We updated SITE_KEY_HCAPTCHA with the universal value 10000000-ffff-ffff-ffff-000000000001 that fits fine for replit because replit is just for development purposes, and we do not need to use the real site key, because the domain changes every time we restart the replit server. So we can use the universal value.

TODO: comment all the operations related to the implementation of the captcha, and the related imports.
"""

"""
JOBS = [
    {
        'id': 1,
        'title': 'Data Analyst',
        'location': 'Bengaluru, India',
        'salary': 'Rs. 10,00,000'
    },
    {
        'id': 2,
        'title': 'Data Scientist',
        'location': 'Delhi, India',
        'salary': 'Rs. 15,00,000'
    },
    {
        'id': 3,
        'title': 'Frontend engineer',
        'location': 'Remote',
        'salary': 'Rs. 12,00,000'
    },
    {
        'id': 4,
        'title': 'Backend engineer',
        'location': 'San Francisco, USA',
        'salary': '$ 120,000'
    },
    {
        'id': 5,
        'title': 'DevOps engineer',
        'location': 'Chicago, USA'
    }
]
"""

"""
def load_jobs_from_db():
    with engine.connect() as conn:
        result = conn.execute(text("select * from jobs"))
        rows = result.mappings().all()
        jobs = [dict(row) for row in rows]
        return jobs
"""

@app.route("/job/<id>/apply", methods=['post'])
def apply_to_job(id):
    #data absorbs all the submitted data in the form
    #from the URL
    #data = request.args
    job=load_job_from_db(id)
    if not hcaptcha.verify():
        flash("Captcha non valido, riprova.")
        render_template(
            'jobpage.html', job=job)
    
    data = request.form
    #job=load_job_from_db(id)
    #This helper function is used to add the application to the       database.
    add_application_to_db(id, data)
    #We can:
    #store the data in the db
    #send an email to the applicant
    #display an aknowledgement
    #here a jsonified version of the data is returned
    #return jsonify(data)
    #rendering a webpage with the data
    return render_template(
        'application_submitted.html', application=data, job=job)
    

@app.route("/job/<id>")
def show_job(id):
    job = load_job_from_db(id)
    #return jsonify(job)
    #return jsonify(jobs[int(id)-1])
    if not job:
        return "Not Found", 404
    return render_template('jobpage.html', job=job,                company_name='Jovian', SITE_KEY_HCAPTCHA=SITE_KEY_HCAPTCHA)

@app.route("/")
#The "/" is the root URL. The root URL is the URL of the home page of a website.
#def hello_world():
def hello_jovian():
    jobs = load_jobs_from_db()
    #return "<p>Hello, World!</p>"
    #We send the list of jobs to the HTML file by passing JOBS     as an argument to the render_template function. The            argument is JOBS but the parameter name could have been        anything.
    """return render_template('home.html', jobs=JOBS,                 company_name='Jovian')"""
    #We replacd the JSON object JOBS with the database object      jobs,which is a list of dictionaries.
    return render_template('home.html', jobs=jobs,                 company_name='Jovian')

print(__name__)

@app.route("/api/jobs")
def list_jobs():
    #return jsonify(JOBS)
    jobs = load_jobs_from_db()
    return jsonify(jobs)
    
"""Instead of using flask run command, we can use app.run command to run the application:"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #print("I am inside the if now") 
"""host='0.0.0.0' means that the app runs on a local development server. debug=True means that the app runs in debug mode. Debug mode is useful for development because it provides useful error messages and restarts the server when code changes. Te check:
if __name__ == '__main__' is used to ensure that the app runs only if the script is executed directly, and not if it is imported as a module in another script."""