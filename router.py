import handler
class Router:
    @staticmethod
    def run(app):
        @app.route('/process', methods=['POST'])
        def process():
            return handler.process()
        
        @app.route('/')
        def home():
            return {
                'message': 'Hello World'
            }