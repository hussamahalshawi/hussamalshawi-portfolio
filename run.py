from App import create_app
# from App.__init__ import create_app


hussam_app_instance = create_app()

if __name__ == '__main__':
    hussam_app_instance.run(debug=True, port=5000)