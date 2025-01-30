from .models import Car


def create_cars():
    car_data = [
        {
            "name": "Toyota Highlander",
            "transmission": "Automatic",
            "car_type": "SUV",
            "rental_price": 100,
            "speed": 120.5,
            "fuel_type": "Gasoline",
            "capacity": 7,
            "year": 2023,
            "active": True,
            "available": True,
            "images": [
                "https://i.pinimg.com/736x/8c/36/b2/8c36b2f339d5b23e66f4a6cfec1d9516.jpg"
            ],
        },
        {
            "name": "Honda Civic",
            "transmission": "Automatic",
            "car_type": "Sedan",
            "rental_price": 80,
            "speed": 150.2,
            "fuel_type": "Gasoline",
            "capacity": 5,
            "year": 2022,
            "active": True,
            "available": True,
            "images": [
                "https://i.pinimg.com/736x/65/c3/63/65c3636ca6b81584e53084c105c7a54d.jpg"
            ],
        },
        {
            "name": "Ford F-150",
            "transmission": "Automatic",
            "car_type": "Truck",
            "rental_price": 120,
            "speed": 130.7,
            "fuel_type": "Diesel",
            "capacity": 6,
            "year": 2024,
            "active": True,
            "available": False,
            "images": [
                "https://i.pinimg.com/736x/63/bc/25/63bc25a9187402b4562947bcf1c69ec0.jpg"
            ],
        },
        {
            "name": "Mercedes Benz C350",
            "transmission": "Manual",
            "car_type": "Sedan",
            "rental_price": 150,
            "speed": 200.3,
            "fuel_type": "Gasoline",
            "capacity": 4,
            "year": 2023,
            "active": True,
            "available": True,
            "images": [
                "https://i.pinimg.com/736x/e1/4c/2a/e14c2aa19c7c889626bf4858e54258b8.jpg"
            ],
        },
    ]
    for car in car_data:
        Car.objects.create(**car)
