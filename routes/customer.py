from flask import (
    Blueprint,
    render_template,
    request,
    redirect,
    session,
    current_app
)

from models import (
    db,
    Vehicle,
    ServiceBooking,
    Complaint,
    RepairStatus,
    RepairGallery,
    Estimate,
    Invoice
)

from werkzeug.utils import secure_filename

from reportlab.pdfgen import canvas
from datetime import datetime

import os

customer = Blueprint(
    "customer",
    __name__
)


#======================
# CUSTOMER DASHBOARD
# ======================

@customer.route("/dashboard")
def dashboard():

    if "user_id" not in session:
        return redirect("/")

    vehicles = Vehicle.query.filter_by(
        owner_id=session["user_id"]
    ).all()

    vehicle_ids = [
        vehicle.id
        for vehicle in vehicles
    ]

    estimates = Estimate.query.filter(
        Estimate.vehicle_id.in_(vehicle_ids)
    ).all()

    invoices = Invoice.query.filter(
        Invoice.vehicle_id.in_(vehicle_ids)
    ).all()
    bookings = ServiceBooking.query.filter(
    ServiceBooking.vehicle_id.in_(vehicle_ids)
    ).all()

    complaints = Complaint.query.filter(
    Complaint.vehicle_id.in_(vehicle_ids)
).all()

    return render_template(
    "customer_dashboard.html",
    vehicles=vehicles,
    estimates=estimates,
    invoices=invoices,
    bookings=bookings,
    complaints=complaints
)
#=======================
#ADD VEHICLE
#=======================
@customer.route("/add_vehicle", methods=["GET","POST"])
def add_vehicle():

    if request.method == "POST":

        vehicle = Vehicle(

            registration_number=request.form["reg"],

            model=request.form["model"],

            odometer=request.form["odo"],

            last_service=request.form["last"],

            next_service="Not Scheduled",

            owner_id=session["user_id"]

        )

        db.session.add(vehicle)
        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "add_vehicle.html"
    )
#======================
#edit_vehicle
#======================
@customer.route("/edit_vehicle/<int:id>",
methods=["GET","POST"])
def edit_vehicle(id):

    vehicle = Vehicle.query.get_or_404(id)

    if vehicle.owner_id != session["user_id"]:
        return redirect("/dashboard")

    if request.method == "POST":

        vehicle.registration_number = request.form["reg"]
        vehicle.model = request.form["model"]
        vehicle.odometer = request.form["odo"]
        vehicle.last_service = request.form["last"]
        vehicle.next_service = request.form["next"]

        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "edit_vehicle.html",
        vehicle=vehicle
    )
#======================
#delete_vehicle
#======================
@customer.route("/delete_vehicle/<int:id>")
def delete_vehicle(id):

    vehicle = Vehicle.query.get_or_404(id)

    if vehicle.owner_id != session["user_id"]:
        return redirect("/dashboard")

    db.session.delete(vehicle)
    db.session.commit()

    return redirect("/dashboard")
#=======================
#BOOK SERVICE
#=======================
@customer.route("/book_service/<int:id>",
methods=["GET","POST"])
def book_service(id):

    if request.method == "POST":

        booking = ServiceBooking(

            vehicle_id=id,

            service_type=request.form["service"],

            booking_date=request.form["date"]

        )

        db.session.add(booking)
        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "book_service.html",
        vehicle_id=id
    )
#=======================
#COMPLAINT PHOTO UPLOAD
#=======================
@customer.route("/complaint/<int:id>",
methods=["GET","POST"])
def complaint(id):

    if request.method == "POST":

        file = request.files["photo"]

        filename = secure_filename(
            file.filename
        )

        file.save(
    os.path.join(
        current_app.config["UPLOAD_FOLDER"],
        filename
    )
)

        c = Complaint(

            vehicle_id=id,

            description=request.form["desc"],

            photo=filename

        )

        db.session.add(c)
        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "complaint.html",
        vehicle_id=id
    )
#======================
#status
#======================
@customer.route("/status/<int:id>")
def status(id):

    repair = RepairStatus.query.filter_by(
        vehicle_id=id
    ).first()

    evidence = RepairGallery.query.filter_by(
        vehicle_id=id
    ).all()

    return render_template(
        "status.html",
        repair=repair,
        evidence=evidence
    )
#======================
#REPAIR TIMELINE GALLERY
#======================
@customer.route("/gallery/<int:vehicle_id>")
def gallery(vehicle_id):

    photos = RepairGallery.query.filter_by(
        vehicle_id=vehicle_id
    ).all()

    return render_template(
        "gallery.html",
        photos=photos
    )

#=======================
#PDF INVOICE GENERATOR
#=====================

@customer.route("/invoice/<int:id>")
def invoice(id):

    invoice = Invoice.query.get(id)

    pdf_path = f"static/invoices/{invoice.invoice_number}.pdf"

    c = canvas.Canvas(pdf_path)

    c.drawString(
        100,
        800,
        "CHENNAI CAR-TECH"
    )

    c.drawString(
        100,
        760,
        f"Invoice No: {invoice.invoice_number}"
    )

    c.drawString(
    100,
    730,
    f"Amount: ₹{invoice.total_amount}"
)

    c.save()

    return redirect("/" + pdf_path)
#=========================
#about us
#==========================
@customer.route("/about")
def about():

    return render_template(
        "about.html"
    )
#=====================
#invoice pdf
#=====================
@customer.route("/invoice_pdf/<int:id>")
def invoice_pdf(id):

    invoice = Invoice.query.get(id)

    pdf_path = (
        f"static/invoices/"
        f"{invoice.invoice_number}.pdf"
    )

    c = canvas.Canvas(pdf_path)

    c.drawString(
        50,800,
        "CHENNAI CAR-TECH"
    )

    c.drawString(
        50,770,
        f"Invoice: "
        f"{invoice.invoice_number}"
    )

    c.drawString(
        50,730,
        f"Labour: "
        f"{invoice.labour_details}"
    )

    c.drawString(
        50,700,
        f"Parts: "
        f"{invoice.parts_details}"
    )

    c.drawString(
        50,670,
        f"Tax: ₹"
        f"{invoice.tax_amount}"
    )

    c.drawString(
        50,640,
        f"Warranty: "
        f"{invoice.warranty_details}"
    )

    c.drawString(
        50,600,
        f"Total: ₹"
        f"{invoice.total_amount}"
    )

    c.save()

    return redirect(
        "/" + pdf_path
    )
#==========================
#update estimation
#=========================
@customer.route("/estimate_action/<int:id>/<action>")
def estimate_action(id, action):

    estimate = Estimate.query.get_or_404(id)

    if action == "approve":
        estimate.customer_response = "Approved"

    elif action == "reject":
        estimate.customer_response = "Rejected"

    elif action == "clarification":
        estimate.customer_response = "Clarification Requested"

    estimate.response_time = datetime.now().strftime(
        "%d-%m-%Y %H:%M:%S"
    )

    db.session.commit()

    return redirect("/finance")
#============================
#edit booking service
#=========================
@customer.route(
    "/edit_booking/<int:id>",
    methods=["GET", "POST"]
)
def edit_booking(id):

    booking = ServiceBooking.query.get_or_404(id)

    if request.method == "POST":

        booking.service_type = request.form["service"]
        booking.booking_date = request.form["date"]

        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "edit_booking.html",
        booking=booking
    )
#==========================
#delete booking service
#======================
@customer.route("/delete_booking/<int:id>")
def delete_booking(id):

    booking = ServiceBooking.query.get_or_404(id)

    db.session.delete(booking)

    db.session.commit()

    return redirect("/dashboard")
#=================
#complain edti
#=====================
@customer.route(
    "/edit_complaint/<int:id>",
    methods=["GET", "POST"]
)
def edit_complaint(id):

    complaint = Complaint.query.get_or_404(id)

    if request.method == "POST":

        complaint.description = request.form["desc"]

        db.session.commit()

        return redirect("/dashboard")

    return render_template(
        "edit_complaint.html",
        complaint=complaint
    )
#==============
#delete complains
#================
@customer.route("/delete_complaint/<int:id>")
def delete_complaint(id):

    complaint = Complaint.query.get_or_404(id)

    db.session.delete(complaint)

    db.session.commit()

    return redirect("/dashboard")
#=========================
# FINANCE PAGE
#=========================
@customer.route("/finance")
def finance():

    vehicles = Vehicle.query.filter_by(
        owner_id=session["user_id"]
    ).all()

    vehicle_ids = [v.id for v in vehicles]

    print("Customer Vehicles:", vehicle_ids)

    estimates = Estimate.query.filter(
        Estimate.vehicle_id.in_(vehicle_ids)
    ).all()

    invoices = Invoice.query.filter(
        Invoice.vehicle_id.in_(vehicle_ids)
    ).all()

    print("Invoice Count:", len(invoices))

    for inv in invoices:
        print(
            inv.invoice_number,
            inv.vehicle_id
        )

    return render_template(
        "finance.html",
        estimates=estimates,
        invoices=invoices
    )