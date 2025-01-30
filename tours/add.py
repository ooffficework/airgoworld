from .models import Tour
def create_mock_data():
    mock_data = [
        {
            "name": "Sunset Resort",
            "status": "active",
            "rating": 4.5,
            "description": "A beautiful resort with breathtaking sunset views.",
            "featured": True,
            "location": "Maldives",
            "display": True,
            "price": 250.000,
            "reviews": 128,
            "images": [
                "https://i.pinimg.com/736x/17/cb/82/17cb82951685bf7d7bb4dee1b6b12024.jpg"
            ]
        },
        {
            "name": "Skyline Borche",
            "status": "featured",
            "rating": 4.8,
            "description": "Luxury hotel located in the heart of the city with skyline views.",
            "featured": True,
            "location": "New York, USA",
            "display": True,
            "price": 350.000,
            "reviews": 200,
            "images": [
                "https://i.pinimg.com/736x/79/bc/31/79bc31411ae1cb6dbfa6c30ad3edd003.jpg"
            ]
        },
        {
            "name": "Ocean Breeze Villas",
            "status": "inactive",
            "rating": 4.2,
            "description": "Relaxing beachfront villas perfect for a serene getaway.",
            "featured": False,
            "location": "Bora Bora",
            "display": False,
            "price": 400.000,
            "reviews": 85,
            "images": [
                "https://i.pinimg.com/736x/91/0b/8d/910b8dd9c8ce374836645f80eb4c442d.jpg"
            ]
        },
        {
            "name": "Mountain Retreat",
            "status": "active",
            "rating": 4.7,
            "description": "Peaceful retreat located in the mountains for nature lovers.",
            "featured": False,
            "location": "Swiss Alps",
            "display": True,
            "price": 300.000,
            "reviews": 150,
            "images": [
                "https://i.pinimg.com/736x/aa/1c/99/aa1c99018dd9cd6248704101e959fe65.jpg"
            ]
        }
    ]
    for data in mock_data:
        Tour.objects.create(**data)  

