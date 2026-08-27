from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from notifications.models import Notification
from .forms import ComplaintForm
from .models import Complaint


@login_required
def my_complaints(request):
    complaints = Complaint.objects.filter(customer=request.user).select_related('booking', 'booking__provider')
    return render(request, 'complaints/my_complaints.html', {'complaints': complaints})


@login_required
def complaint_create(request):
    form = ComplaintForm(request.POST or None, user=request.user)
    if request.method == 'POST' and form.is_valid():
        complaint = form.save(commit=False)
        complaint.customer = request.user
        complaint.save()
        for admin_user in complaint.customer.__class__.objects.filter(is_staff=True):
            Notification.objects.create(
                user=admin_user,
                title='New complaint submitted',
                message=f'{request.user.username} submitted a complaint: {complaint.category}.',
                link='/admin/complaints/complaint/',
            )
        messages.success(request, 'Complaint submitted for review.')
        return redirect('complaints:my_complaints')
    return render(request, 'complaints/complaint_form.html', {'form': form})

# Create your views here.
