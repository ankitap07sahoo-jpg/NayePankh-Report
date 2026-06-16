import bcrypt
from datetime import date
from database.connection import get_session, get_engine
from database.models import Base, User, Volunteer, Beneficiary, Donation, Program

def seed():
    print("Initializing Database...")
    engine = get_engine()
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    session = get_session()
    
    # 1. Admin & Viewer Users
    admin_hash = bcrypt.hashpw('nayepankh@2024'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    viewer_hash = bcrypt.hashpw('viewer123'.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
    
    admin = User(username='admin', password_hash=admin_hash, role='admin')
    viewer = User(username='viewer', password_hash=viewer_hash, role='viewer')
    session.add_all([admin, viewer])
    
    # 2. Volunteers
    v1 = Volunteer(name="Rahul Sharma", email="rahul@example.com", phone="9876543210", city="Delhi", skills="Teaching", join_date=date(2024, 1, 15))
    v2 = Volunteer(name="Priya Patel", email="priya@example.com", phone="9876543211", city="Mumbai", skills="Social Media", join_date=date(2024, 2, 10))
    session.add_all([v1, v2])
    
    # 3. Beneficiaries
    b1 = Beneficiary(name="Raju", age=12, gender="Male", education_level="Primary", location="Delhi Slums", status="active")
    b2 = Beneficiary(name="Sunita", age=15, gender="Female", education_level="Secondary", location="Mumbai Dharavi", status="active")
    session.add_all([b1, b2])
    
    # 4. Donations
    d1 = Donation(donor_name="TechCorp India", amount=50000, date=date(2024, 4, 1), purpose="Education", payment_mode="Bank Transfer")
    d2 = Donation(donor_name="Anil Gupta", amount=5000, date=date(2024, 4, 15), purpose="General", payment_mode="UPI")
    session.add_all([d1, d2])
    
    # 5. Programs
    p1 = Program(title="Evening Pathshala", description="Daily classes", start_date=date(2024, 1, 1), end_date=date(2024, 12, 31), status="ongoing")
    session.add(p1)
    
    session.commit()
    
    # Link
    p1.beneficiaries.append(b1)
    session.commit()
    
    print("Database seeded successfully with users (admin, viewer) and demo data.")
    session.close()

if __name__ == "__main__":
    seed()
