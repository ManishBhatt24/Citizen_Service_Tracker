from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.db.models import Count, Q
from .models import Complaint, CATEGORIES, STATUS_CHOICES

def dashboard(request):
    total = Complaint.objects.count()
    pending = Complaint.objects.filter(status='Pending').count()
    in_progress = Complaint.objects.filter(status='In Progress').count()
    resolved = Complaint.objects.filter(status='Resolved').count()

    category_rows = (
        Complaint.objects.values('category')
        .annotate(count=Count('category'))
        .order_by('-count')
    )

    recent = Complaint.objects.all()[:8]

    return render(request, "dashboard.html", {
        "total": total,
        "pending": pending,
        "in_progress": in_progress,
        "resolved": resolved,
        "categories": category_rows,
        "recent": recent
    })

def register(request):
    if request.method == "POST":
        name = request.POST.get("citizen_name", "").strip()
        phone = request.POST.get("phone", "").strip()
        email = request.POST.get("email", "").strip()
        category = request.POST.get("category", "").strip()
        description = request.POST.get("description", "").strip()
        location = request.POST.get("location", "").strip()

        if not name or not phone or not category or not description or not location:
            messages.error(request, "Please fill all required fields.")
            return redirect("register")

        if category not in CATEGORIES:
            messages.error(request, "Invalid complaint category.")
            return redirect("register")

        if len(description) < 10:
            messages.error(request, "Description must contain at least 10 characters.")
            return redirect("register")

        if not phone.isdigit() or len(phone) < 7 or len(phone) > 15:
            messages.error(request, "Enter a valid phone number.")
            return redirect("register")

        complaint = Complaint.objects.create(
            citizen_name=name,
            phone=phone,
            email=email if email else None,
            category=category,
            description=description,
            location=location
        )

        messages.success(request, f"Complaint registered successfully. Complaint ID: #{complaint.id}")
        return redirect("complaints")

    return render(request, "register.html", {"categories": CATEGORIES})

def complaints(request):
    search = request.GET.get("search", "").strip()
    category = request.GET.get("category", "").strip()
    status = request.GET.get("status", "").strip()

    qs = Complaint.objects.all()

    if search:
        is_numeric = search.isdigit()
        if is_numeric:
            qs = qs.filter(
                Q(citizen_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(location__icontains=search) |
                Q(description__icontains=search) |
                Q(id=int(search))
            )
        else:
            qs = qs.filter(
                Q(citizen_name__icontains=search) |
                Q(phone__icontains=search) |
                Q(location__icontains=search) |
                Q(description__icontains=search)
            )

    if category in CATEGORIES:
        qs = qs.filter(category=category)

    if status in STATUS_CHOICES:
        qs = qs.filter(status=status)

    return render(request, "complaints.html", {
        "complaints": qs,
        "categories": CATEGORIES,
        "statuses": STATUS_CHOICES,
        "selected_category": category,
        "selected_status": status,
        "search": search
    })

def update_status(request, complaint_id):
    if request.method == "POST":
        new_status = request.POST.get("status", "")
        if new_status not in STATUS_CHOICES:
            messages.error(request, "Invalid status.")
            return redirect("complaints")

        complaint = get_object_or_404(Complaint, pk=complaint_id)
        complaint.status = new_status
        complaint.save()

        messages.success(request, f"Complaint #{complaint_id} status updated to {new_status}.")
    return redirect("complaints")

def category_data(request):
    rows = (
        Complaint.objects.values('category')
        .annotate(count=Count('category'))
    )
    return JsonResponse({
        "labels": [r["category"] for r in rows],
        "values": [r["count"] for r in rows]
    })
