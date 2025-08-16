from flask import Flask, render_template, jsonify

#An App is an object of Flask class. It is our WSGI application. WSGI stands for Web Server Gateway Interface.
#In any python script, you have this variable __name__ which is a built-in variable.
"""this variable refers to how a particular script was invoked. In this case the script was invoked as the main script. That's why __main__ is the value of __name__ variable."""
app = Flask(__name__)

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

@app.route("/")
#The "/" is the root URL. The root URL is the URL of the home page of a website.
#def hello_world():
def hello_jovian():
    #return "<p>Hello, World!</p>"
    #We send the list of jobs to the HTML file by passing JOBS as an argument to the render_template function. The argument is JOBS but the parameter name could have been anything.
    return render_template('home.html', jobs=JOBS, company_name='Jovian')
print(__name__)

@app.route("/jobs")
def list_jobs():
    return jsonify(JOBS)
    
"""Instead of using flusk run command, we can use app.run command to run the application:"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #print("I am inside the if now") 
"""host='0.0.0.0' means that the app runs on a local development server. debug=True means that the app runs in debug mode. Debug mode is useful for development because it provides useful error messages and restarts the server when code changes. Te check:
if __name__ == '__main__' is used to ensure that the app runs only if the script is executed directly, and not if it is imported as a module in another script."""