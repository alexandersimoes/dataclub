import sys
sys.path.insert(0, '/web/test.dataviva.info')

from dataviva import app as application

from werkzeug.debug import DebuggedApplication
application = DebuggedApplication(application, True)
