from application import application

from spectacle.frontend.views import *
from spectacle.document.views import *
from spectacle.full_text_search.views import *
from spectacle.user.views import *

if __name__ == '__main__':
    application.run(host='0.0.0.0')
