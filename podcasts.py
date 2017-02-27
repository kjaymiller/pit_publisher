from models import Podcast, iTunes, Google, RSS
from config import OWNER

pitpodcast = Podcast(title='Productivity in Tech Podcast',
        links=[iTunes('https://itunes.apple.com/us/podcast/productivity-in-tech-podcast/id1086437786?mt=2'),
                Google('https://play.google.com/music/listen#/ps/Isoopwbe6zdbev5ijenegkcpp44'),
                RSS('https://feedpress.me/pitpodcast')],
        collection='pitpodcast',
        abbreviation='PIT',
        uuid='13f11d77-78cd-4c25-822a-6308b0558ea2',
        description='Jay Miller sits down with people in tech that love what \
they and figures out how the secret to how they get it all done!',
        owner=OWNER,
        categories=('Technology', 'Business', 'Society &amp; Culture'),
        image_href='http://productivityintech.com/files/images/pitpodcast_logo_itunes.png',
        subtitle='Learning Productivity from People like Us!',
        keywords=['productivity', 'technology', 'motiviation', 'interviews', 'tools'],
        new_feed ='http://feedpress.me/pitpodcast')

pitreflections = Podcast(title='Productivity in Tech: Reflections',
        links=[iTunes('https://itunes.apple.com/us/podcast/productivity-in-tech-reflections/id1161292423'),
            Google('https://play.google.com/music/m/Isz5woinrsifpk6o5xrffozrgl4'),
            RSS('https://feedpress.me/pitreflections')],
        collection='pitreflections',
        abbreviation='Reflection',
        uuid='70d65953-a4fe-4a6e-a4ca-7975853771ab',
        description='Reflections from founder of Productivity in Tech, Jay \
Miller. This podcast was created to encourage you to start thinking about what happened in your day and what you can learn from it.',
        owner=OWNER,
        categories=('Technology', 'Society &amp; Culture'), # Add Personal Journals Back
        image_href='http://productivityintech.com/files/images/PITReflections.png',
        subtitle='',
        keywords=['productivity', 'coaching', 'motivation', 'journaling'],
        new_feed='http://feedpress.me/pitreflections')

podcasts = {'pitpodcast':pitpodcast, 'pitreflections':pitreflections}
