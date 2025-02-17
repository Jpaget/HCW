Local host to run dynamic pages:

If you’re opening the rankings.html directly in your browser (file:// protocol), the fetch request might not work due to cross-origin restrictions. You’ll need to serve the files using a local server.
You can use Python's built-in HTTP server to do this. Navigate to your project directory in the terminal/command prompt, and run:

python -m http.server 
This will start a local server at http://localhost:8000/, and you can access rankings.html by going to http://localhost:8000/rankings.html.


python -m http.server 8000