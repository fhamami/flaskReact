from webapp import db
from webapp.models import Post

db.drop_all()

db.create_all()

post1 = Post('Slow-Cooker Tacos', 'Delicious ground beef that has been simmering in taco seasoning and sauce.  Perfect with hard-shelled tortillas!')
post2 = Post('Hamburgers', 'Classic dish elivated with pretzel buns.')
post3 = Post('Mediterranean Chicken', 'Grilled chicken served with pitas, hummus, and sauted vegetables.')
db.session.add(post1)
db.session.add(post2)
db.session.add(post3)

db.session.commit()
