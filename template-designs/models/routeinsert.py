from models.route import Route


d = [
        {"depcity": "addisababa",
        "decity": "dredawa",
        "kilometer": 545, 
        "price": 450,
        "plate_no": 56545
        }
        ]
for i in d:
    t = Route(**i)
    t.save()


