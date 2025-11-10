from server import create_app, db

app = create_app()

@app.route('/')
def index():
    return {'message': 'Camping Fun API'}

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(port=5555, debug=True)