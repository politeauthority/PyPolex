if __name__ == '__main__':
    from app import app
    app.run(
	host = "0.0.0.0",
        port = 8070, 
        debug = app.config['DEBUG']
    )
