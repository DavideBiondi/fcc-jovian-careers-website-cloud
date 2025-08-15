from flask import Flask, render_template

#An App is an object of Flask class. It is our WSGI application. WSGI stands for Web Server Gateway Interface.
#In any python script, you have this variable __name__ which is a built-in variable.
"""this variable refers to how a particular script was invoked. In this case the script was invoked as the main script. That's why __main__ is the value of __name__ variable."""
app = Flask(__name__)

"""The route() function of the Flask class is a decorator, which tells the application which URL should call the associated function. In this case, the URL of the given function (hello_world) is '/'.
We tell Flask when a certain URL is requested, the function is called and the return value of the function is sent to the browser as a response. In this case we registering a route, which is simply a part of the URL after the domain name. For example, if you go to www.example.com/hello, the path of the route is /hello.
And the domain name is www.example.com.

The symbol '@' is a decorator. A decorator is a design pattern in Python that allows a user to add new functionality to an existing object without modifying its structure. Decorators are usually called before the definition of a function you want to decorate."""
@app.route("/")
#The "/" is the root URL. The root URL is the URL of the home page of a website.
def hello_world():
    #return "<p>Hello, World!</p>"
    return render_template('home.html')
print(__name__)
"""Instead of using flusk run command, we can use app.run command to run the application:"""
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
    #print("I am inside the if now") 
"""host='0.0.0.0' means that the app runs on a local development server. debug=True means that the app runs in debug mode. Debug mode is useful for development because it provides useful error messages and restarts the server when code changes. Te check:
if __name__ == '__main__' is used to ensure that the app runs only if the script is executed directly, and not if it is imported as a module in another script."""