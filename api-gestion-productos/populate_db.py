#!/usr/bin/env python3
"""Script to populate the database with sample data for testing."""

import sys
from datetime import datetime, timedelta
from pathlib import Path

# Add src to path
BASE_DIR = Path(__file__).parent / "src"
sys.path.insert(0, str(BASE_DIR))

from models.database import Product, ProductCategoryEnum, User, UserRoleEnum
from models.db import SessionLocal
from utils.security import hash_password


def create_sample_data():
    """Create sample users and products for testing."""
    db = SessionLocal()

    try:
        # Check if data already exists
        if db.query(User).first():
            print("✅ Sample data already exists")
            return

        print("📝 Creating sample data...")

        # Create admin user
        admin_user = User(
            nombre="Admin User",
            email="admin@example.com",
            password_hash=hash_password("Admin123!"),
            rol=UserRoleEnum.ADMIN
        )
        db.add(admin_user)

        # Create client user
        client_user = User(
            nombre="Client User",
            email="client@example.com",
            password_hash=hash_password("Client123!"),
            rol=UserRoleEnum.CLIENT
        )
        db.add(client_user)

        # Create sample products
        future_date = datetime.utcnow() + timedelta(days=30)

        products_data = [
            {
                "nombre": "Manzana Roja",
                "categoria": ProductCategoryEnum.FRUTAS,
                "cantidad": 100,
                "precio": 2.50,
                "fecha_vencimiento": future_date
            },
            {
                "nombre": "Leche Entera",
                "categoria": ProductCategoryEnum.LACTEOS,
                "cantidad": 50,
                "precio": 1.80,
                "fecha_vencimiento": future_date + timedelta(days=7)
            },
            {
                "nombre": "Pan Integral",
                "categoria": ProductCategoryEnum.GRANOS,
                "cantidad": 25,
                "precio": 3.20,
                "fecha_vencimiento": future_date - timedelta(days=20)  # Almost expired
            },
            {
                "nombre": "Zanahoria",
                "categoria": ProductCategoryEnum.VERDURAS,
                "cantidad": 75,
                "precio": 1.20,
                "fecha_vencimiento": future_date + timedelta(days=14)
            },
            {
                "nombre": "Queso Cheddar",
                "categoria": ProductCategoryEnum.LACTEOS,
                "cantidad": 30,
                "precio": 5.50,
                "fecha_vencimiento": future_date + timedelta(days=45)
            }
        ]

        for product_data in products_data:
            product = Product(**product_data)
            db.add(product)

        db.commit()
        print("✅ Sample data created successfully!")
        print("\n👤 Test Users:")
        print("   Admin: admin@example.com / Admin123!")
        print("   Client: client@example.com / Client123!")
        print("\n📦 Sample Products:")
        for product_data in products_data:
            print(f"   - {product_data['nombre']} ({product_data['cantidad']} units)")

    except Exception as e:
        db.rollback()
        print(f"❌ Error creating sample data: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_sample_data()
