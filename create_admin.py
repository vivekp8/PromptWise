import bcrypt
from modules.database import SessionLocal, User

def create_admin():
    db = SessionLocal()
    try:
        username = "admin"
        email = "admin@promptwise.com"
        password = "adminpassword123"
        
        # Check existing
        existing_user = db.query(User).filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            print(f"User {username} or {email} already exists.")
            if existing_user.role != "admin":
                existing_user.role = "admin"
                db.commit()
                print("Updated role to admin.")
            else:
                print("Already admin.")
            return

        # Hash with bcrypt
        hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        admin_user = User(
            username=username,
            email=email,
            hashed_password=hashed,
            role="admin",
            full_name="System Administrator",
            provider="local"
        )
        db.add(admin_user)
        db.commit()
        print(f"Admin user '{username}' created successfully.")
    
    except Exception as e:
        print(f"Error creating admin user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin()
