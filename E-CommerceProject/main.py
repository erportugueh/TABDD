from website import create_app  # Import the create_app function from the website module/package

app = create_app()  # Instantiate the Flask app by calling the create_app function

# Launch site
if __name__ == '__main__':  # Ensure this block runs only when the script is executed directly
    app.run(debug=True)  # Run the Flask app with debugging enabled for easier development
