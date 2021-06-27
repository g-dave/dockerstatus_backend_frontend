from dockerstatusapi import app

#just for Dev Environment
#app.run(host='0.0.0.0', port=80, debug=True)

from waitress import serve
serve(app, host="0.0.0.0", port=80)