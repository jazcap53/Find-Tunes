import urllib.parse
from sqlalchemy import create_engine

escaped_pw = urllib.parse.quote_plus('kaZ00bie!do')
# print(escaped_pw)

engine = create_engine('postgresql+psycopg2://jazcap53:' + escaped_pw + '@localhost:5432/tunes')

