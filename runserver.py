from testsuite import main

app, socketio = main()
socketio.run(app, host='0.0.0.0', port=5000, debug=True, use_reloader=True)
