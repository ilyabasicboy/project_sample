from tordoors_new.custom_catalog.models import Section, Product, Category, ItemType, Facing

for i in range(30):
    Section.objects.create(title='Раздел' + str(i+1), slug='razdel' + str(i+1), item_type=ItemType.objects.all().first())
for i in range(150):
    Product.objects.create(title='Товар ' + str(i + 1), slug='tovar' + str(i + 1), price=1000*(i+1), facing=Facing.objects.all().first())