from django.http import JsonResponse
from django.shortcuts import render

from diagn.forms import DiagnForm
from diagn.models import Diagn
from django.views.decorators.csrf import csrf_exempt

from datetime import datetime
import matplotlib.pyplot as plt
import io
from django.http import HttpResponse
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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


def select_date(request):
    return render(request, 'select_date.html')


def plot_diagn_by_date(request):
    date_str = request.GET.get('date')
    if not date_str:
        return HttpResponse("Дата не вказана", status=400)

    try:
        date = datetime.strptime(date_str, '%Y-%m-%d').date()
    except ValueError:
        return HttpResponse("Неправильний формат дати", status=400)

    # Отримання даних з бази даних
    data = Diagn.objects.filter(date_comit=date).order_by('time_comit')
    if not data:
        return HttpResponse("Дані для цієї дати не знайдено.", status=404)

    times = [record.time_comit.strftime('%H:%M:%S') for record in data]
    gpu_temps = [record.gpu_t for record in data]
    processor_temps = [record.processor_t for record in data]

    # Створення графіка
    fig, ax = plt.subplots()
    ax.plot(times, gpu_temps, marker='o', label='GPU Temperature')
    ax.plot(times, processor_temps, marker='x', label='Processor Temperature')

    ax.set_xlabel('Час')
    ax.set_ylabel('Температура (°C)')
    ax.set_title(f'Температура GPU та процесора протягом часу для {date}')
    ax.legend()

    # Збереження графіка в буфер пам'яті
    buffer = io.BytesIO()
    canvas = FigureCanvas(fig)
    canvas.print_png(buffer)
    plt.close(fig)  # Закрити фігуру, щоб звільнити пам'ять

    # Повернення графіка як зображення PNG
    return HttpResponse(buffer.getvalue(), content_type='image/png')