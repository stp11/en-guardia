#!/usr/bin/env python3
"""
CLI command to create admin users for the admin panel.
Usage: python -m commands.create_user create <username> <password>
"""

import sys

from sqlmodel import Session, select

from database import engine
from models import Users


def create_user(username: str, password: str, is_admin: bool = True) -> bool:
    """Create a new admin user."""
    with Session(engine) as session:
        statement = select(Users).where(Users.username == username)
        existing_user = session.exec(statement).first()

        if existing_user:
            print(f"❌ User '{username}' already exists!")
            return False

        user = Users(
            username=username,
            password_hash=Users.hash_password(password),
            is_admin=is_admin,
            is_active=True,
        )

        session.add(user)
        session.commit()
        session.refresh(user)

        print(f"✅ User '{username}' created successfully!")
        print(f"   User ID: {user.id}")
        print(f"   Created at: {user.created_at}")
        return True


def main():
    if len(sys.argv) < 2:
        print("📚 User Management")
        print("Usage:")
        print("  python -m commands.create_user create <username> <password>")
        return

    command = sys.argv[1]

    if command == "create":
        if len(sys.argv) != 4:
            print(
                "❌ Usage: python create_admin.py create <username> <password>"
            )
            return
        username, password = sys.argv[2], sys.argv[3]
        create_user(username, password)

    else:
        print(f"❌ Unknown command: {command}")
        print("Available commands: create")


if __name__ == "__main__":
    main()
