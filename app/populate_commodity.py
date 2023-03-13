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

if not Type.objects.filter(name='Bag').exists():
    t3 = Type.objects.create(name='Bag')
    t3.save()
else:
    t3 = Type.objects.get(name='Bag')

if not Type.objects.filter(name='Clothing').exists():
    t4 = Type.objects.create(name='Clothing')
    t4.save()
else:
    t4 = Type.objects.get(name='Clothing')

if not Type.objects.filter(name='Others').exists():
    t5 = Type.objects.create(name='Others')
    t5.save()
else:
    t5 = Type.objects.get(name='Others')


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
    type=t5,
)

commodity6 = Commodities.objects.create(
    c_id=6,
    c_name='T-Shirt',
    price=20.99,
    description='',
    image='static/images/Commodities/T-Shirt.png',
    type=t4,
)

commodity7 = Commodities.objects.create(
    c_id=7,
    c_name='Switch',
    price=220.99,
    description='Nintendo Switch Neon Red/Neon Blue with Mario Kart 8 Deluxe and 3 Month Nintendo Switch Online Membership',
    image='static/images/Commodities/Switch.png',
    type=t1,
)

commodity8 = Commodities.objects.create(
    c_id=8,
    c_name='Backpack',
    price=299.99,
    description='Gomatic Laptop Bag Backpack - 20L to 30L Expandable Business Travel Back Pack, Anti Theft & TSA Approved, Hand Underseat Luggage or Cabin Carry On, The Most Functional Water Resistant Rucksack Ever',
    image='static/images/Commodities/Backpack.png',
    type=t3,
)

commodity9 = Commodities.objects.create(
    c_id=9,
    c_name='Bag',
    price=29.95,
    description='AviiatoR® Hot Food Delivery Bag With Divider Thermal Insulated 40*40*35cm For Indian, Kebabs, Chinese, Pizza For Restaurants, Couriers, Picnic Cooler Bag, Groceries Boot Organiser Catering Warm Bags',
    image='static/images/Commodities/Bag.png',
    type=t3,
)

commodity10 = Commodities.objects.create(
    c_id=10,
    c_name='Shoes',
    price=179.99,
    description='Timberland Mens 6 Inch WR Basic Fashion Boots',
    image='static/images/Commodities/Shoes.png',
    type=t3,
)

commodity11 = Commodities.objects.create(
    c_id=11,
    c_name='Watch',
    price=157.98,
    description='Timberland Dress Watch TBL15951JSB.03',
    image='static/images/Commodities/Watch.png',
    type=t5,
)

commodity12 = Commodities.objects.create(
    c_id=12,
    c_name='Record_player',
    price=69.99,
    description='',
    image='static/images/Commodities/Record_player.png',
    type=t1,
)

# Save the products to the database
commodity1.save()
commodity2.save()
commodity3.save()
commodity4.save()
commodity5.save()
commodity6.save()
commodity7.save()
commodity8.save()
commodity9.save()
commodity10.save()
commodity11.save()
commodity12.save()

print('Commodity created successfully!')




