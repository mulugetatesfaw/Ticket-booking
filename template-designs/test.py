from models.bus import Bus
from models.base import BaseModel

data = [
{
"plate_no": 33289,
"sideno": 2012,
"no_seats": 65
},
{
"plate_no": 67566,
"sideno": 3520,
"no_seats": 65
}
]


for d in data:
    p = Bus(**d)
    p.save()
