import os
from django.shortcuts import render
from django.conf import settings
from app.components.treaty_uploader import save_uploaded_file
from app.components.optimizer_engine import run_treaty_optimizer
from app.components.report_generator import generate_summary_plot

from django.core.mail import send_mail
from django.conf import settings

# app/views.py (Add this at the top or bottom)

def contact_success(request):
    return render(request, "contact_success.html")

def product(request):
    return render(request, "product.html")
    
def technology(request):
    return render(request, "technology.html")

def home(request):
    return render(request, "home.html")


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        message = request.POST.get("message")

        full_message = f"Message from {name} <{email}>:\n\n{message}"

        send_mail(
            subject="Contact Form Submission",
            message=full_message,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=["your_email@yourdomain.com"],
        )
        return render(request, "contact_success.html")

    return render(request, "contact.html")


def about(request):
    founder_bio = {
        "name": "Stella Dong",
        "title": "Founder & CEO",
        "photo": "img/founder.jpg",
        "bio": (
            "With a background in AI and actuarial science, Stella brings deep expertise "
            "in RL-based financial modeling. She previously led pricing algorithm development "
            "at Prescryptive Health and holds a PhD in computational neuroscience."
        )
    }
    return render(request, "about.html", {"founder": founder_bio})


def product_view(request):
    optimization = None
    if request.method == 'POST' and request.FILES.get('treaty_file'):
        treaty_file = request.FILES['treaty_file']
        saved_path = save_uploaded_file(treaty_file)

        # Run PPO + LLM optimizer
        optimization = run_treaty_optimizer(saved_path)

        # Plot rewards, save as image
        plot_path = generate_summary_plot(optimization['rewards'])
        plot_url = os.path.relpath(plot_path, settings.BASE_DIR / 'app' / 'static')

        optimization = {
            'retention': optimization['retention'],
            'limit': optimization['limit'],
            'llm_summary': optimization['llm_summary'],
            'plot_url': f'/static/{plot_url}',
        }

    return render(request, 'product.html', {'optimization': optimization})
