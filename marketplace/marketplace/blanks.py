# Роли пользователей
roles = {
    'buyer': {
        'name': 'buyer',
        'permissions': ['view_user', 'change_user', 'view_product'],
    },
    'seller': {
        'name': 'seller',
        'permissions': ['view_user', 'change_user', 'view_product', 'add_product', 'change_product', 'delete_product'],
    },
    'pvz': { # Владелец пункта выдачи заказов
        'name': 'pvz',
        'permissions': ['view_user', 'change_user', 'view_product', 'add_product', 'change_product', 'delete_product'],
    }
}

# Категории товаров
categories = {
    'Электроника': {
        'name': 'Electronics',
        'description': 'Technical devices such as smartphones, laptops, headphones, and accessories.'
    },
    'Одежда': {
        'name': 'Clothing',
        'description': 'Men\'s, women\'s, and children\'s clothing: t-shirts, jeans, dresses, jackets, etc.'
    },
    'Обувь': {
        'name': 'Footwear',
        'description': 'Sneakers, shoes, boots, sandals, and other footwear for all ages.'
    },
    'Аксессуары': {
        'name': 'Accessories',
        'description': 'Bags, belts, watches, jewelry, and other accessories.'
    },
    'Красота и уход': {
        'name': 'Beauty & Personal Care',
        'description': 'Cosmetics, skincare, haircare, and body care products.'
    },
    'Дом и интерьер': {
        'name': 'Home & Interior',
        'description': 'Furniture, decor, textiles, and home improvement items.'
    },
    'Кухонные принадлежности': {
        'name': 'Kitchenware',
        'description': 'Cookware, kitchen appliances, knives, and cooking accessories.'
    },
    'Бытовая техника': {
        'name': 'Home Appliances',
        'description': 'Refrigerators, washing machines, vacuum cleaners, and other household appliances.'
    },
    'Спорт и активный отдых': {
        'name': 'Sports & Outdoors',
        'description': 'Sports equipment, workout clothing, and outdoor gear.'
    },
    'Игры и игрушки': {
        'name': 'Games & Toys',
        'description': 'Board games, construction sets, plush toys, and educational kits for children.'
    },
    'Книги и канцелярия': {
        'name': 'Books & Stationery',
        'description': 'Fiction, textbooks, notebooks, pens, and other stationery items.'
    },
    'Автотовары': {
        'name': 'Automotive',
        'description': 'Car parts, car accessories, and car care products.'
    },
    'Зоотовары': {
        'name': 'Pet Supplies',
        'description': 'Pet food, toys, accessories, and care products for pets.'
    },
    'Продукты питания': {
        'name': 'Groceries',
        'description': 'Groceries, beverages, snacks, canned goods, and other food products.'
    },
    'Здоровье и медицина': {
        'name': 'Health & Medicine',
        'description': 'Vitamins, medicines, medical devices, and health care products.'
    },
    'Детские товары': {
        'name': 'Baby Products',
        'description': 'Diapers, baby food, strollers, toys, and accessories for babies.'
    },
    'Цифровые товары': {
        'name': 'Digital Goods',
        'description': 'E-books, software, online courses, and subscriptions.'
    },
    'Хобби и творчество': {
        'name': 'Hobbies & Crafts',
        'description': 'Craft kits, painting supplies, modeling kits, and other hobby materials.'
    },
    'Ювелирные изделия': {
        'name': 'Jewelry',
        'description': 'Rings, earrings, bracelets, pendants, and other jewelry items.'
    },
    'Эко-товары': {
        'name': 'Eco-Friendly Products',
        'description': 'Eco-friendly products such as reusable bottles, bags, and cleaning supplies.'
    },
    'Сезонные товары': {
        'name': 'Seasonal Goods',
        'description': 'Holiday items such as Christmas decorations, Easter sets, etc.'
    },
    'Элитные товары': {
        'name': 'Luxury Goods',
        'description': 'Designer clothing, accessories, watches, and other luxury items.'
    },
    'Цветы и подарки': {
        'name': 'Flowers & Gifts',
        'description': 'Bouquets, gift sets, greeting cards, and souvenirs.'
    },
    'Строительство и ремонт': {
        'name': 'Construction & Tools',
        'description': 'Tools, construction materials, plumbing, and electrical supplies.'
    },
    'Музыкальные инструменты': {
        'name': 'Musical Instruments',
        'description': 'Guitars, keyboards, drums, and other musical instruments.'
    },
    'Товары для офиса': {
        'name': 'Office Supplies',
        'description': 'Office equipment, paper, folders, and other office supplies.'
    },
    'Товары для сада и дачи': {
        'name': 'Garden & Outdoor',
        'description': 'Garden tools, plants, outdoor furniture, and accessories.'
    },
    'Товары для путешествий': {
        'name': 'Travel Gear',
        'description': 'Luggage, backpacks, travel pillows, and other travel accessories.'
    },
    'Товары для вечеринок': {
        'name': 'Party Supplies',
        'description': 'Decorations, tableware, costumes, and party accessories.'
    },
    'Товары для рукоделия': {
        'name': 'Craft Supplies',
        'description': 'Yarn, fabrics, paints, and other materials for crafting.'
    }
}