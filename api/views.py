from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.views import View
from django.utils.decorators import method_decorator
from django.contrib.auth.hashers import make_password, check_password
import json
from .models import Parent, Child, Registration
from django.core.files.storage import default_storage
import os
import tempfile

try:
    import PyPDF2
except ImportError:
    PyPDF2 = None

# Create your views here.

def health_check(request):
    """Health check endpoint for deployment monitoring"""
    return JsonResponse({'status': 'healthy', 'message': 'KidAI Backend is running'})

@method_decorator(csrf_exempt, name='dispatch')
class RegisterView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            # Extract fields
            child_name = data.get('child_name')
            child_dob = data.get('child_dob')
            child_group = data.get('child_group', '')
            parent_name = data.get('parent_name')
            parent_dob = data.get('parent_dob')
            parent_mobile = data.get('parent_mobile')
            password = data.get('password')

            # Basic validation
            if not all([child_name, child_dob, parent_name, parent_dob, parent_mobile, password]):
                return JsonResponse({'error': 'All fields are required.'}, status=400)

            # Create or get Parent
            parent, _ = Parent.objects.get_or_create(
                mobile_number=parent_mobile,
                defaults={
                    'name': parent_name,
                    'date_of_birth': parent_dob,
                }
            )
            # Create Child
            child = Child.objects.create(
                name=child_name,
                date_of_birth=child_dob,
                age_group=child_group
            )
            # Hash password
            password_hash = make_password(password)
            # Create Registration
            Registration.objects.create(
                parent=parent,
                child=child,
                password_hash=password_hash
            )
            return JsonResponse({'success': True, 'message': 'Registration successful.'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            parent_mobile = data.get('parent_mobile')
            password = data.get('password')
            if not parent_mobile or not password:
                return JsonResponse({'error': 'Both fields are required.'}, status=400)
            # Find parent
            try:
                parent = Parent.objects.get(mobile_number=parent_mobile)
            except Parent.DoesNotExist:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
            # Find registration(s) for this parent
            regs = Registration.objects.filter(parent=parent)
            if not regs.exists():
                return JsonResponse({'error': 'No registration found for this parent.'}, status=401)
            # Check password against any registration (all children share parent password)
            valid = False
            for reg in regs:
                if check_password(password, reg.password_hash):
                    valid = True
                    break
            if not valid:
                return JsonResponse({'error': 'Invalid credentials.'}, status=401)
            # Get all children for this parent
            children = [
                {'id': reg.child.id, 'name': reg.child.name}
                for reg in regs
            ]
            return JsonResponse({'success': True, 'children': children, 'parent_name': parent.name})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)

@method_decorator(csrf_exempt, name='dispatch')
class SummarizeView(View):
    def post(self, request):
        if 'file' not in request.FILES:
            return JsonResponse({'error': 'No file uploaded.'}, status=400)
        file = request.FILES['file']
        ext = os.path.splitext(file.name)[1].lower()
        text = ''
        if ext == '.pdf' and PyPDF2:
            with tempfile.NamedTemporaryFile(delete=False, suffix='.pdf') as tmp:
                for chunk in file.chunks():
                    tmp.write(chunk)
                tmp_path = tmp.name
            with open(tmp_path, 'rb') as f:
                reader = PyPDF2.PdfReader(f)
                for page in reader.pages:
                    text += page.extract_text() or ''
            os.remove(tmp_path)
        elif ext in ['.txt', '.md']:
            text = file.read().decode('utf-8')
        else:
            return JsonResponse({'error': 'Unsupported file type.'}, status=400)
        # TODO: Replace with real AI summarization
        summary = text[:500] + ('...' if len(text) > 500 else '')
        return JsonResponse({'summary': summary})
