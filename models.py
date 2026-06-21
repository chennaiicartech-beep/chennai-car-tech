from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
# ======================
# USER TABLE
# ======================

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True)

    password = db.Column(db.String(200))

    role = db.Column(db.String(20))
    # admin / customer


# ======================
# VEHICLE TABLE
# ======================

class Vehicle(db.Model):
    id = db.Column(db.Integer, primary_key=True)

    registration_number = db.Column(db.String(50))
    model = db.Column(db.String(100))

    odometer = db.Column(db.String(50))

    last_service = db.Column(db.String(50))
    next_service = db.Column(db.String(50))

    owner_id = db.Column(
        db.Integer,
        db.ForeignKey("user.id")
    )
# ======================
# SERVICE BOOKING
# ======================

class ServiceBooking(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(db.Integer)

    service_type = db.Column(db.String(100))

    booking_date = db.Column(db.String(50))

    status = db.Column(
        db.String(50),
        default="Pending"
    )


# ======================
# COMPLAINTS
# ======================

class Complaint(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(db.Integer)

    description = db.Column(db.String(500))

    photo = db.Column(db.String(300))


# ======================
# REPAIR STATUS
# ======================

class RepairStatus(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(db.Integer)

    status = db.Column(
        db.String(100),
        default="Pending"
    )
 
#=======================
#Service History
#======================
class ServiceHistory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(db.Integer)

    service_date = db.Column(db.String(50))

    service_details = db.Column(db.String(500))

    amount = db.Column(db.Float)
#======================
#Inventory Management
#=======================
class Inventory(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    part_name = db.Column(db.String(100))

    quantity = db.Column(db.Integer)

    price = db.Column(db.Float)
#======================
#Revenue Dashboard
#=======================
class Payment(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    amount = db.Column(db.Float)

    date = db.Column(db.String(50))
#=======================
#Notifications
#=======================
class Notification(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    user_id = db.Column(db.Integer)

    message = db.Column(db.String(300))

    is_read = db.Column(
        db.Boolean,
        default=False
    )
    #======================
#Repair Gallery database
#======================
class RepairGallery(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vehicle_id = db.Column(db.Integer)

    file_name = db.Column(
        db.String(300)
    )

    file_type = db.Column(
        db.String(50)
    )
    # image/video

    stage = db.Column(
        db.String(100)
    )
    # Before Repair
    # During Repair
    # After Repair

    remarks = db.Column(
        db.String(500)
    )

    upload_time = db.Column(
        db.String(100)
    )
#=======================
#Estimate database
#=======================
class Estimate(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    vehicle_id = db.Column(db.Integer)

    parts_cost = db.Column(db.Float)

    labour_cost = db.Column(db.Float)

    taxes = db.Column(db.Float)

    total_amount = db.Column(db.Float)

    notes = db.Column(db.String(500))

    status = db.Column(
        db.String(50),
        default="Pending"
    )

    customer_response = db.Column(
        db.String(100),
        default="Waiting"
    )

    response_time = db.Column(
        db.String(100)
    )
#=======================
#Invoice
#=======================
class Invoice(db.Model):

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    vehicle_id = db.Column(db.Integer)

    invoice_number = db.Column(
        db.String(50)
    )

    labour_details = db.Column(
        db.String(500)
    )

    labour_amount = db.Column(
        db.Float
    )

    parts_details = db.Column(
        db.String(500)
    )

    parts_amount = db.Column(
        db.Float
    )

    tax_amount = db.Column(
        db.Float
    )

    warranty_details = db.Column(
        db.String(500)
    )

    total_amount = db.Column(
        db.Float
    )

    created_date = db.Column(
        db.String(50)
    )