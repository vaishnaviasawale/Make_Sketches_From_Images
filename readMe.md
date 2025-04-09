<br /><b>MAKE SKETCHES FROM IMAGES </b>

<br /><b>csv2</b> cv2 is the module import name for the "opencv-python" library, which provides access to the functionalities of the OpenCV (Open Source Computer Vision Library) for image processing and computer vision tasks. 

<br /><b>os</b> This module provides a portable way of using operating system dependent functionality like creating, opening, and reading files and folders.

<br /><b>Werkzeug</b> Werkzeug is a comprehensive WSGI web application library. It began as a simple collection of various utilities for WSGI applications and has become one of the most advanced WSGI utility libraries. Werkzeug doesn’t enforce any dependencies. It is up to the developer to choose a template engine, database adapter, and even how to handle requests.

<br /><b>Secure Filename</b> https://medium.com/@sujathamudadla1213/what-is-the-use-of-secure-filename-in-flask-9eef4c71503b 

<br /><b>INSTRUCTIONS</b>
<br />pip install virtualenv

<br />python -m virtualenv env (creating a virtual environment named env so that an instance of python is created)

<br />go to powershell -> Set-ExecutionPolicy unrestricted -> A

<br />.\env\Scripts\activate.ps1 to activate the environment (ps1 because we want to activate in the powershell terminal)

<br />pip install flask # Flask is a Python module that allows us to build web apps

<br />pip install opencv-python # to use cv2

<br /><b>STEPS TO DEPLOY ON REPLIT</b>

<br />1. Go to replit.com and sign up
<br />2. Click on ‘Create App’ and create one with the Python template
<br />3. Add all the necessary files and folders from this repo
<br />4. Configure Replit by searching for a .replit file and modify it to start the app with “app.py” (instead of main.py)
<br />5. On the left pan, under ‘Tools’, search for ‘Secret’ to add our secrets as a .env file (CLOUD_NAME, API_KEY, and API_SECRET needed to upload images to Cloudinary)
<br />6. On the left pane, under ‘Tools’ open the ‘Shell’. Run ‘pip install -r requirements.txt’ to install all needed packages
<br />7. Click on ‘Run’ at the top of the page. Under the Webview, we can see a preview of our website.
<br />8. Click on ‘Deploy’. We get a temporary Dev URL of the type https://your-repl-name.username.repl.co .This is a public URL and can be used by anyone. To set a custom domain, Replit will give you a CNAME record to set in your domain registrar (like GoDaddy, Namecheap, etc.). We need to own a domain (can be bought from any registrar), update DNS records (Replit will guide), and then wait a few minutes to an hour for it to go live. This also needs a paid plan.
