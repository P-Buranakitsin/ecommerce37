import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce37.settings')
django.setup()

from app.models import Commodities,Type

if not Type.objects.filter(name='Electronic').exists():
    t1 = Type.objects.create(name='Electronic')
    t1.save()
else:
    t1 = Type.objects.get(name='Electronic')

if not Type.objects.filter(name='Fruit').exists():
    t2 = Type.objects.create(name='Fruit')
    t2.save()
else:
    t2 = Type.objects.get(name='Fruit')

if not Type.objects.filter(name='Others').exists():
    t3 = Type.objects.create(name='Others')
    t3.save()
else:
    t3 = Type.objects.get(name='Others')


commodity1 = Commodities.objects.create(
    c_id=1,
    c_name='Orange',
    price=10.00,
    description='This is the description for Orange.',
    image='static/images/Commodities/Orange.png',
    type=t2,
)

commodity2 = Commodities.objects.create(
    c_id=2,
    c_name='Cherry',
    price=10.00,
    description='This is the description for Cherry.',
    image='static/images/Commodities/Cherry.png',
    type=t2,
)

commodity3 = Commodities.objects.create(
    c_id=3,
    c_name='Headphone',
    price=49.99,
    description='This is the description for Headphone.',
    image='static/images/Commodities/Headphone.png',
    type=t1,
)

commodity4 = Commodities.objects.create(
    c_id=4,
    c_name='iPhone8',
    price=154.99,
    description='Apple iPhone 8, 64GB, Red (Renewed).',
    image='static/images/Commodities/iPhone8.png',
    type=t1,
)

commodity5 = Commodities.objects.create(
    c_id=5,
    c_name='Cleanser',
    price=4.99,
    description='CeraVe Hydrating Cleanser for Normal to Dry Skin 473ml with Hyaluronic Acid & 3 Essential Ceramides.',
    image='static/images/Commodities/Cleanser.png',
    type=t3,
)

commodity6 = Commodities.objects.create(
    c_id=6,
    c_name='T-Shirt',
    price=20.99,
    description='',
    image='static/images/Commodities/T-Shirt.png',
    type=t3,
)

# Save the products to the database
commodity1.save()
commodity2.save()
commodity3.save()
commodity4.save()
commodity5.save()
commodity6.save()

print('Commodity created successfully!')




