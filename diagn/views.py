from django.http import JsonResponse
from django.shortcuts import render

from diagn.forms import DiagnForm
from diagn.models import Diagn
from django.views.decorators.csrf import csrf_exempt


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
#             return redirect('/login/')
# data = {'date_comit': current_date, 'time_comit': current_time,
#                         'terminal_name': computer_name, 'gpu_t': gpu_t,
#                         'processor_t': processor_t, 'processor_load': processor_load,
#                         'memori_load': memori_load,'user_id': int(user_id)}

# def parcel_form(request):
#     if request.method == 'POST':
#         form = ParcelForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return HttpResponse('form.save()')
#         else:
#             # form = ParcelForm()
#             form = ParcelForm(initial={'sender': request.user.username})
#
#             return render(request, 'parcel_form.html', context={'form': form})
#             # return HttpResponse('not form.save()')
#     # form = ParcelForm()
#     form = ParcelForm(initial={'sender': request.user.username})
#     return render(request, 'parcel_form.html', context={'form':form})
