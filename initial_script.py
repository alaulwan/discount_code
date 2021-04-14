from discount_code.api.discount_code.models import Client
from discount_code.api.discount_code.models import Brand
from discount_code.api.discount_code.models import DiscountCode
from discount_code.api.discount_code.models import UserDiscontRelation

import datetime

client_admin = None
try:
    client_admin = Client.objects.get(username='admin')
except Client.DoesNotExist:
    client_admin = Client.objects.create_superuser('admin', 'admin@myproject.com', 'admin')
    client_admin.save()

client2 = None
try:
    client2 = Client.objects.get(username='alaa')
except Client.DoesNotExist:
    client2 = Client.objects.create_user(username='alaa', email="alaa@app.se", password='alaa')
    client2.save()

client3 = None
try:
    client3 = Client.objects.get(username='brand')
except Client.DoesNotExist:
    client3 = Client.objects.create_user(username='brand', email="alaa@app.se", password='brand')
    client3.is_brand = True
    client3.save()

client4 = None
try:
    client4 = Client.objects.get(username='omar')
except Client.DoesNotExist:
    client4 = Client.objects.create_user(username='omar', email="omar@app.se", password='omar')
    client4.save()

brand = None
try:
    brand = Brand.objects.get(brand_name='HM')
except Brand.DoesNotExist:
    brand = Brand(brand_name='HM', owner_id=client3)
    brand.save()

discountCode = None
try:
    discountCode = DiscountCode.objects.get(brand_id=brand, value='XXX')
except DiscountCode.DoesNotExist:
    d = datetime.datetime.now()
    discountCode = DiscountCode(value='XXX', discount_percent=20, expired_at=d, brand_id=brand)
    discountCode.save()

try:
    discountCode2 = DiscountCode.objects.get(brand_id=brand, value='ZZZ')
except DiscountCode.DoesNotExist:
    d = datetime.datetime.now()
    discountCode2 = DiscountCode(value='ZZZ', discount_percent=30, expired_at=d, brand_id=brand)
    discountCode2.save()

userDiscontRelation = None
try:
    userDiscontRelation = UserDiscontRelation.objects.get(discount_id=discountCode, user_id=client2)
except UserDiscontRelation.DoesNotExist:
    userDiscontRelation = UserDiscontRelation(user_id=client2, discount_id=discountCode)
    userDiscontRelation.save()

print("Done")
