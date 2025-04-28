from django.shortcuts import render, redirect
from .services.capture_service import CaptureService

def capture_camera(request):
    if request.method == 'POST':
        capture_service = CaptureService()
        capture_service.capture_from_camera()
        return redirect('capture_camera')

    return render(request, 'detection/capture.html')
