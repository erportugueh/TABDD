from website import create_app
import test

app = create_app()

# Launch site
if __name__ == '__main__':
    app.run(debug=True)
