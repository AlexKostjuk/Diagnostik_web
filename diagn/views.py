from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
import base64
from diagn.forms import DiagnForm
from diagn.models import Diagn
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
import matplotlib.dates as mdates

# Create your views here.
@csrf_exempt
def to_bd(request):
    if request.method == 'POST':
        form = DiagnForm(request.POST)
        if form.is_valid():
            diagn_data = Diagn.objects.create(date_comit=form.cleaned_data['date_comit'],
                                            time_comit=form.cleaned_data['time_comit'],
                                            terminal_name=form.cleaned_data['terminal_name'],
                                            gpu_t=form.cleaned_data['gpu_t'],
                                            processor_t=form.cleaned_data['processor_t'],
                                            processor_load=form.cleaned_data['processor_load'],
                                            memori_load=form.cleaned_data['memori_load'],
                                            user_id=form.cleaned_data['user_id'],

                                            )
            diagn_data.save()
            print(diagn_data)
            return JsonResponse({'to_db': True})
        else:
            return JsonResponse({'error': 'Invalid request method'}, status=400)

@login_required(login_url='/login')
def select_date(request):
    dates = Diagn.objects.filter(user_id=request.user).values_list('date_comit', flat=True).distinct()
    return render(request, 'select_date.html', {'dates': dates})

def plot_diagn_by_date(request):
    if not request.user.is_authenticated:
        return HttpResponse("Ви повинні бути авторизовані, щоб переглядати дані.", status=401)

    date_str = request.GET.get('date')
    if not date_str:
        return HttpResponse("Дата не вказана", status=400)

    try:
        date = datetime.strptime(date_str, '%b. %d, %Y').date()
    except ValueError:
        return HttpResponse("Неправильний формат дати", status=400)

    data = Diagn.objects.filter(date_comit=date, user_id=request.user).order_by('time_comit')
    if not data:
        return HttpResponse("Дані для цієї дати не знайдено.", status=404)

    times = [datetime.combine(date, record.time_comit) for record in data]
    gpu_temps = [record.gpu_t for record in data]
    processor_temps = [record.processor_t for record in data]

    fig, ax = plt.subplots()
    ax.plot(times, gpu_temps, marker='o', label='GPU Temperature')
    ax.plot(times, processor_temps, marker='x', label='Processor Temperature')

    ax.set_xlabel('Час')
    ax.set_ylabel('Температура (°C)')
    ax.set_title(f'Температура GPU та процесора протягом часу для {date}')
    ax.legend()

    ax.xaxis.set_major_locator(mdates.MinuteLocator(interval=30))
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%H:%M'))
    plt.xticks(rotation=45)

    buffer = io.BytesIO()
    plt.savefig(buffer, format='png')
    plt.close(fig)
    buffer.seek(0)

    image_png = buffer.getvalue()
    buffer.close()

    image_base64 = base64.b64encode(image_png).decode('utf-8')

    return render(request, 'plot.html', {'image_base64': image_base64})





def home(request):
    return render(request, 'home.html')