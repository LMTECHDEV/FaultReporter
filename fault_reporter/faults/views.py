from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from .models import Fault
from .forms import FaultForm
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader, simpleSplit
import os

def fault_list(request):
    faults = Fault.objects.all()
    if request.method == 'POST':
        saved_any = False
        # Process all forms based on form IDs
        for key in request.POST.keys():
            if key.startswith('location_'):
                form_id = key.split('_')[1]
                form_data = {
                    'location': request.POST.get(f'location_{form_id}', ''),
                    'description': request.POST.get(f'description_{form_id}', ''),
                    'image1': request.FILES.get(f'image1_{form_id}'),
                    'image2': request.FILES.get(f'image2_{form_id}'),
                    'image3': request.FILES.get(f'image3_{form_id}'),
                    'image4': request.FILES.get(f'image4_{form_id}'),
                    'image5': request.FILES.get(f'image5_{form_id}'),
                }
                if (form_data['location'] or form_data['description'] or 
                    form_data['image1'] or form_data['image2'] or 
                    form_data['image3'] or form_data['image4'] or form_data['image5']):
                    form = FaultForm(form_data, files=form_data)
                    if form.is_valid():
                        form.save()
                        saved_any = True
        if saved_any:
            return redirect('fault_list')
    return render(request, 'faults/fault_list.html', {'faults': faults, 'form': FaultForm()})

def delete_fault(request, fault_id):
    fault = get_object_or_404(Fault, id=fault_id)
    fault.delete()
    return redirect('fault_list')

def generate_pdf(request):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="fault_report.pdf"'

    p = canvas.Canvas(response, pagesize=letter)
    width, height = letter
    margin = 50
    y = height - margin
    faults = Fault.objects.all()

    for index, fault in enumerate(faults, start=1):
        if y < 150:
            p.showPage()
            y = height - margin

        # Title
        p.setFont("Helvetica-Bold", 12)
        p.drawString(margin, y, f"Fault {index}")
        y -= 20

        # Location
        p.setFont("Helvetica", 12)
        p.drawString(margin, y, f"Location: {fault.location}")
        y -= 20

        # Description (wrapped)
        desc_text = f"Description: {fault.description}"
        desc_lines = simpleSplit(desc_text, 'Helvetica', 12, width - 2 * margin)
        for line in desc_lines:
            p.drawString(margin, y, line)
            y -= 15
        y -= 10

        # Helper function to draw an image safely
        def draw_image(image_path, label):
            nonlocal y
            try:
                img = ImageReader(image_path)
                img_width, img_height = img.getSize()
                scale = min(400.0 / img_width, 200.0 / img_height)
                scaled_height = img_height * scale

                # Add page if not enough room
                if y - scaled_height < margin:
                    p.showPage()
                    y = height - margin

                p.drawImage(img, margin, y - scaled_height, width=img_width * scale, height=scaled_height)
                y -= scaled_height + 20
            except Exception as e:
                p.drawString(margin, y, f"{label} Error: {str(e)}")
                y -= 20

        # Process up to 5 images
        for i in range(1, 6):
            img_field = f'image{i}'
            img = getattr(fault, img_field, None)
            if img:
                draw_image(img.path, img_field.capitalize())

        y -= 20

        if y < 50:
            p.showPage()
            y = height - margin

    p.showPage()
    p.save()
    return response