"""
The Base Configuration file IS
"""

from datetime import datetime

# DATABASE_URL = 'example.com'
# USERNAME = 'myusername'
# PASSWORD = 'DON'T_SHARE_THIS_WITH_OTHERS>'
# PORT = 27017 (DEFAULT: Recommended that you change your defaul port)
# DATABASE = 'database' This is the database that you use for your content
# WEBSITE_URL = 'The URL for your website'
# COMPANY = 'Name of the Company used in copywright inofmation'
# OWNER = {name: Owner McOwnerface, Owner is the primary submitter for the site
#          email: owner@email.com,
#          uri: personalwebsite.com}
# AUTHORS Same configuration as the Owner but for other contributors
# AUTHORS['OWNER'] = OWNER #TOLD YOU. Don't remove this line
# RECOMMENDED: Each Owner should be the same as the name.
# DEFAULT_UPLOAD_SOURCE = 'posts' Where files are stored prior to being uploaded
# FILES_PATH = 'files' Where static files on the website are stored
# FEED_LOCATION = f'{FILES_PATH}/feed.xml' blog post
# FEED_ICON = f'{FILES_PATH}/images/feed_icon.png'
# FEED_LOGO = f'{FILES_PATH}/image/feed_logo.png'

# GENERATOR INFORMATION - DO NOT EDIT
GENERATOR_URI ='https://github.com/kjaymiller/podcast_publisher'
GENERATOR_NAME = 'Productivity in Tech RSS Generator'

#DB INFORMATION
DATABASE_URL = 'productivityintech.com'
USERNAME = 'kjaymiller'
PASSWORD = '[@TtToWdmeTAo*DqbKnkw2'
PORT = 36161
DATABASE = 'pitpodcast'

# FILE MANAGEMENT
DEFAULT_UPLOAD_SOURCE = 'posts'
FILES_PATH = 'files'

# FEED INFORMATION
FEED_LOCATION = f'{FILES_PATH}/feed.xml'
FEED_ICON = f'{FILES_PATH}/images/feed_icon.png'
FEED_LOGO = f'{FILES_PATH}/image/feed_logo.png'

#COPYRIGHT INFO - FOR FEEDS AND WEBSITE
year = datetime.now().year
FEED_COPYRIGHT = f'© {year}'

# COMPANY INFORMATION
COMPANY = 'Productivity in Tech'
WEBSITE_URL = 'https://productivityintech.com'

#OWNER INFORMATION
OWNER = {'name': 'Jay Miller',
        'email': 'kjaymiller@gmail.com',
        'uri':'http://productivityintech.com'}

# DO NOT INCLUDE THE OWNER, IT IS ADDED LATER
AUTHORS = {'Johan Gustaphzon':{
                    'name': 'Johan Gustaphzon',
                    'email':'gustaphzon@gmx.com',
                    'uri':'http://appleyra.se'
                    },
            'Tiffany White' : {
                    'name': 'Tiffany White',
                    'email': 'tiffany@thatmacnerd.com',
                    'uri': 'https://thatmacnerd.com'
                    }
                }
AUTHORS['OWNER'] = OWNER #TOLD YOU. Don't remove this line
