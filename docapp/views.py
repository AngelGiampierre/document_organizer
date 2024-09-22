from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import JsonResponse
import os
import shutil
from datetime import datetime, timedelta

@csrf_exempt
def document_organizer(request):
    if request.method == 'POST':
        # Organize next path folder:
        path_folder = request.POST.get('path_folder', '')

        if path_folder:
            files = os.listdir(path_folder)
            if files:
                for file in files:
                    file_path = os.path.join(path_folder, file)
                    if file.endswith('.exe'):
                        # Executable File Management
                        executable_folder = os.path.join(path_folder, 'executable')
                        if not os.path.exists(executable_folder):
                            os.makedirs(executable_folder)
                        
                        dest_file_path = os.path.join(executable_folder, file)
                        
                        if os.path.isfile(file_path):
                            shutil.move(file_path, dest_file_path)
                            print(f"File {file} moved to folder executable")
                    
                    else:
                        if os.path.isfile(file_path):
                            try:
                                # Weekly Document Organization
                                create_weekly_folders(file_path, path_folder)
                            except Exception as e:
                                print('Error: ', e)

        return JsonResponse({'message': 'Done'}, status=200)
    
    return JsonResponse({'error': 'Invalid method request'}, status=405)

def create_weekly_folders(file_path, path_folder):
    mod_time = os.path.getmtime(file_path)
    mod_date = datetime.fromtimestamp(mod_time)
    
    start_of_week = mod_date - timedelta(days=mod_date.weekday())  # Monday
    end_of_week = start_of_week + timedelta(days=6)  # Sunday

    week_folder_name = f"week_{start_of_week.strftime('%d_%m')}_to_{end_of_week.strftime('%d_%m')}"
    week_folder_path = os.path.join(path_folder, week_folder_name)
    
    if not os.path.exists(week_folder_path):
        os.makedirs(week_folder_path)

    shutil.move(file_path, week_folder_path)