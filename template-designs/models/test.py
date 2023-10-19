from bus import Bus
from base import BaseModel

data = [
{
"plate_no": 29565,
"sideno": 3535,
"noseats": 65
},
{
"plate_no": 29566,
"sideno": 3537,
"noseats": 65
}
]


for d in data:
    p = Bus(**d)
    p.save()
