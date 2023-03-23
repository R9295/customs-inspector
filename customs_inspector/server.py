from bottle import ServerAdapter


class Server(ServerAdapter):
    server = None
    quiet = True

    def run(self, handler):
        from wsgiref.simple_server import WSGIRequestHandler, make_server

        class QuietHandler(WSGIRequestHandler):
            def log_request(*args, **kw):
                pass

        self.options['handler_class'] = QuietHandler
        self.server = make_server(self.host, self.port, handler, **self.options)
        self.server.serve_forever()

    def stop(self):
        self.server.server_close()
        self.server.shutdown()
