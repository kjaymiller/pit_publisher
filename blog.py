"""This is the blog configuration script.
You can provide the necessary information for your blog below."""

from models import Blog
from config import AUTHORS

# Enter Blog Information
blog = Blog(
    # title=Blog Title
    title='Productivity in Tech Blog',
    # subtitle: "The Subtitle of the Blog"
    subtitle='Posts from the Productivity in Tech Blog.',
    # uuid='A unique ID for the blog. Use https://www.uuidgenerator.net to generate a uuid'
    uuid='97c7907f-1503-48ce-b37f-6cbfeff1d042',
    # collection='what this blog will be saved as in the mongo database'
    collection='blog'
)
