from flask import send_from_directory

class StaticController:
    
    def serve_static(self, filename):
        return send_from_directory('static', filename)