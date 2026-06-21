from flask import Blueprint, render_template, request, redirect, session
from datetime import datetime
from models import (
    db,
    User,
    Vehicle,
    ServiceBooking,
    Complaint,
    RepairStatus,
    RepairGallery,
    Estimate,
    Invoice
)

from flask import current_app
from werkzeug.utils import secure_filename

from datetime import datetime
import random

import os

admin_bp = Blueprint("admin", __name__)

# ======================
# ADMIN DASHBOARD
# ======================

@admin_bp.route("/admin")
def admin():

    users = User.query.filter_by(
        role="customer"
    ).all()

    vehicles = Vehicle.query.all()

    total_customers = User.query.filter_by(
        role="customer"
    ).count()

    total_vehicles = Vehicle.query.count()

    total_bookings = ServiceBooking.query.count()

    total_complaints = Complaint.query.count()

    open_repairs = RepairStatus.query.filter(
        RepairStatus.status != "Completed"
    ).count()

    completed_repairs = RepairStatus.query.filter_by(
        status="Completed"
    ).count()

    return render_template(
        "admin_dashboard.html",
        users=users,
        vehicles=vehicles,
        total_customers=total_customers,
        total_vehicles=total_vehicles,
        total_bookings=total_bookings,
        total_complaints=total_complaints,
        open_repairs=open_repairs,
        completed_repairs=completed_repairs
    )

#=======================
# ADMIN UPDATE STATUS
#=======================
@admin_bp.route(
    "/update_status/<int:id>",
    methods=["GET", "POST"]
)
def update_status(id):

    repair = RepairStatus.query.filter_by(
        vehicle_id=id
    ).first()

    if request.method == "POST":

        if not repair:

            repair = RepairStatus(
                vehicle_id=id,
                status=request.form["status"]
            )

            db.session.add(repair)

        else:

            repair.status = request.form["status"]

        db.session.commit()

        return redirect(
            f"/vehicle_details/{id}"
        )

    return render_template(
        "update_status.html",
        repair=repair,
        vehicle_id=id
    )

#======================
# UPLOAD REPAIR EVIDENCE
#======================
@admin_bp.route(
    "/upload_repair/<int:vehicle_id>",
    methods=["GET", "POST"]
)
def upload_repair(vehicle_id):

    if request.method == "POST":

        uploaded_file = request.files["file"]

        filename = secure_filename(
            uploaded_file.filename
        )

        uploaded_file.save(
            os.path.join(
                current_app.config["UPLOAD_FOLDER"],
                filename
            )
        )

        extension = filename.split(".")[-1].lower()

        if extension in [
            "jpg",
            "jpeg",
            "png",
            "gif",
            "webp"
        ]:
            file_type = "image"
        else:
            file_type = "video"

        evidence = RepairGallery(

            vehicle_id=vehicle_id,

            file_name=filename,

            file_type=file_type,

            stage=request.form["stage"],

            remarks=request.form["remarks"],

            upload_time=datetime.now().strftime(
                "%d-%m-%Y %H:%M"
            )

        )

        db.session.add(evidence)
        db.session.commit()

        return redirect(
            f"/vehicle_details/{vehicle_id}"
        )

    return render_template(
        "upload_repair.html",
        vehicle_id=vehicle_id
    )
#======================
#Admin Create Estimate
#=======================

@admin_bp.route(
"/create_estimate/<int:vehicle_id>",
methods=["GET","POST"]
)
def create_estimate(vehicle_id):

    if request.method == "POST":

        parts = float(
            request.form["parts_cost"]
        )

        labour = float(
            request.form["labour_cost"]
        )

        taxes = float(
            request.form["taxes"]
        )

        total = parts + labour + taxes

        estimate = Estimate(

            vehicle_id=vehicle_id,

            parts_cost=parts,

            labour_cost=labour,

            taxes=taxes,

            total_amount=total,

            notes=request.form["notes"]

        )

        db.session.add(estimate)
        db.session.commit()

        return redirect("/admin")

    return render_template(
        "create_estimate.html"
    )
#======================
#invoice
#=====================
@admin_bp.route(
"/create_invoice/<int:vehicle_id>",
methods=["GET","POST"]
)
def create_invoice(vehicle_id):

    if request.method == "POST":

        labour_amount = float(
            request.form["labour_amount"]
        )

        parts_amount = float(
            request.form["parts_amount"]
        )

        tax_amount = float(
            request.form["tax_amount"]
        )

        total = (
            labour_amount
            + parts_amount
            + tax_amount
        )

        invoice = Invoice(

            vehicle_id=vehicle_id,

            invoice_number=
            f"CCT-{random.randint(1000,9999)}",

            labour_details=
            request.form["labour_details"],

            labour_amount=
            labour_amount,

            parts_details=
            request.form["parts_details"],

            parts_amount=
            parts_amount,

            tax_amount=
            tax_amount,

            warranty_details=
            request.form["warranty_details"],

            total_amount=
            total,

            created_date=
            datetime.now().strftime(
                "%d-%m-%Y"
            )

        )

        db.session.add(invoice)
        db.session.commit()

        return redirect("/admin")

    return render_template(
        "create_invoice.html"
    )
#===========================
#customer details
#===============================
@admin_bp.route("/customer_details/<int:user_id>")
def customer_details(user_id):

    customer = User.query.get_or_404(user_id)

    vehicles = Vehicle.query.filter_by(
        owner_id=user_id
    ).all()

    return render_template(
        "customer_details.html",
        customer=customer,
        vehicles=vehicles
    )
#===========================
#vehical details
#===========================
@admin_bp.route("/vehicle_details/<int:vehicle_id>")
def vehicle_details(vehicle_id):

    vehicle = Vehicle.query.get_or_404(vehicle_id)

    bookings = ServiceBooking.query.filter_by(
        vehicle_id=vehicle_id
    ).all()

    complaints = Complaint.query.filter_by(
        vehicle_id=vehicle_id
    ).all()

    repairs = RepairGallery.query.filter_by(
        vehicle_id=vehicle_id
    ).all()

    estimates = Estimate.query.filter_by(
        vehicle_id=vehicle_id
    ).all()

    invoices = Invoice.query.filter_by(
        vehicle_id=vehicle_id
    ).all()

    repair_status = RepairStatus.query.filter_by(
        vehicle_id=vehicle_id
    ).first()

    return render_template(
        "vehicle_details.html",
        vehicle=vehicle,
        bookings=bookings,
        complaints=complaints,
        repairs=repairs,
        estimates=estimates,
        invoices=invoices,
        repair_status=repair_status
    )
#===================
#repair states delete
#====================
@admin_bp.route(
    "/delete_status/<int:vehicle_id>"
)
def delete_status(vehicle_id):

    status = RepairStatus.query.filter_by(
        vehicle_id=vehicle_id
    ).first()

    if status:
        db.session.delete(status)
        db.session.commit()

    return redirect(
        f"/vehicle_details/{vehicle_id}"
    )
#=================
#Edit Repair Evidence
#=====================
@admin_bp.route(
    "/delete_evidence/<int:id>"
)
def delete_evidence(id):

    evidence = RepairGallery.query.get_or_404(id)

    vehicle_id = evidence.vehicle_id

    db.session.delete(evidence)

    db.session.commit()

    return redirect(
        f"/vehicle_details/{vehicle_id}"
    )
#================
#Delete Estimate
#=================
@admin_bp.route(
    "/delete_estimate/<int:id>"
)
def delete_estimate(id):

    estimate = Estimate.query.get_or_404(id)

    vehicle_id = estimate.vehicle_id

    db.session.delete(estimate)

    db.session.commit()

    return redirect(
        f"/vehicle_details/{vehicle_id}"
    )
#==================
#Edit Estimate
#=================
@admin_bp.route(
    "/edit_estimate/<int:id>",
    methods=["GET","POST"]
)
def edit_estimate(id):

    estimate = Estimate.query.get_or_404(id)

    if request.method == "POST":

        estimate.parts_cost = float(
            request.form["parts_cost"]
        )

        estimate.labour_cost = float(
            request.form["labour_cost"]
        )

        estimate.taxes = float(
            request.form["taxes"]
        )

        estimate.total_amount = (
            estimate.parts_cost
            + estimate.labour_cost
            + estimate.taxes
        )

        estimate.notes = request.form["notes"]

        db.session.commit()

        return redirect(
            f"/vehicle_details/{estimate.vehicle_id}"
        )

    return render_template(
        "edit_estimate.html",
        estimate=estimate
    )
#==================
#Delete Invoice
#=================
@admin_bp.route(
    "/delete_invoice/<int:id>"
)
def delete_invoice(id):

    invoice = Invoice.query.get_or_404(id)

    vehicle_id = invoice.vehicle_id

    db.session.delete(invoice)

    db.session.commit()

    return redirect(
        f"/vehicle_details/{vehicle_id}"
    )
#=====================
#Edit Invoice
#=====================
@admin_bp.route(
    "/edit_invoice/<int:id>",
    methods=["GET","POST"]
)
def edit_invoice(id):

    invoice = Invoice.query.get_or_404(id)

    if request.method == "POST":

        invoice.labour_details = request.form["labour_details"]

        invoice.parts_details = request.form["parts_details"]

        invoice.labour_amount = float(
            request.form["labour_amount"]
        )

        invoice.parts_amount = float(
            request.form["parts_amount"]
        )

        invoice.tax_amount = float(
            request.form["tax_amount"]
        )

        invoice.warranty_details = request.form[
            "warranty_details"
        ]

        invoice.total_amount = (
            invoice.labour_amount
            + invoice.parts_amount
            + invoice.tax_amount
        )

        db.session.commit()

        return redirect(
            f"/vehicle_details/{invoice.vehicle_id}"
        )

    return render_template(
        "edit_invoice.html",
        invoice=invoice
    )
#=========================
#customer page
#=====================
@admin_bp.route("/customers")
def customers():

    users = User.query.filter_by(
        role="customer"
    ).all()

    return render_template(
        "customers.html",
        users=users
    )
#======================
#edit evidence
#=======================
@admin_bp.route(
    "/edit_evidence/<int:id>",
    methods=["GET", "POST"]
)
def edit_evidence(id):

    evidence = RepairGallery.query.get_or_404(id)

    if request.method == "POST":

        evidence.stage = request.form["stage"]
        evidence.remarks = request.form["remarks"]

        db.session.commit()

        return redirect(
            f"/vehicle_details/{evidence.vehicle_id}"
        )

    return render_template(
        "edit_evidence.html",
        evidence=evidence
    )