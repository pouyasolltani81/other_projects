# import os
# from django.http import HttpResponse
# from django.shortcuts import render
# from django.conf import settings
# from datetime import datetime

# LOG_FILE_PATH = os.path.join(settings.BASE_DIR, 'logs/user_activity.log')

# def download_logs(request):
#     """Serve the log file for download"""
#     return serve_log_file(LOG_FILE_PATH, 'user_activity.log')

# def filter_logs(request):
#     """Filter logs by date or user"""
#     if request.method == 'POST':
#         start_date = request.POST.get('start_date')
#         end_date = request.POST.get('end_date')
#         user = request.POST.get('user')

#         logs = filter_log_file(LOG_FILE_PATH, start_date, end_date, user)
#         return HttpResponse(logs, content_type='text/plain')
    
#     return render(request, 'logmanager/filter_logs.html')

# def serve_log_file(file_path, filename):
#     """Serve a file to the client"""
#     with open(file_path, 'r') as f:
#         file_data = f.read()

#     response = HttpResponse(file_data, content_type='application/octet-stream')
#     response['Content-Disposition'] = f'attachment; filename={filename}'
#     return response

# def filter_log_file(log_path, start_date, end_date, user):
#     """Filter logs based on date and user"""
#     filtered_logs = []
#     with open(log_path, 'r') as file:
#         logs = file.readlines()

#         for log in logs:
#             log_date_str = log.split(" ")[0]
#             log_user = log.split(" ")[-1]
#             log_date = datetime.strptime(log_date_str, "%Y-%m-%d")

#             if (not start_date or log_date >= datetime.strptime(start_date, "%Y-%m-%d")) and \
#                (not end_date or log_date <= datetime.strptime(end_date, "%Y-%m-%d")) and \
#                (not user or user in log_user):
#                 filtered_logs.append(log)

#     return "\n".join(filtered_logs)
# logmanager/views.py


# logmanager/views.py
# logmanager/views.py
# logmanager/views.py
from django.shortcuts import render
from django.http import HttpResponse
import os
from datetime import datetime

LOG_FILE_PATH = os.path.join('logs', 'user_activity.log')

def filter_logs(request):
    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        user = request.POST.get('user')
        include_all_users = request.POST.get('include_all_users')

        print(f"Start Date: {start_date}, End Date: {end_date}, User: {user}, Include All Users: {include_all_users}")

        filtered_logs = filter_log_file(LOG_FILE_PATH, start_date, end_date, user, include_all_users)

        print(f"Filtered Logs: {filtered_logs}")

        if 'download' in request.POST:
            response = HttpResponse(filtered_logs, content_type='text/plain')
            response['Content-Disposition'] = 'attachment; filename=user_activity_filtered.log'
            return response

        return render(request, 'logmanager/filter_logs.html', {
            'logs': filtered_logs,
            'start_date': start_date,
            'end_date': end_date,
            'user': user,
            'include_all_users': include_all_users
        })
    else:
        return render(request, 'logmanager/filter_logs.html')

def download_logs(request):
    """Handles downloading the complete log file."""
    try:
        with open(LOG_FILE_PATH, 'r') as file:
            log_content = file.read()

        print(f"Log Content Length: {len(log_content)}")  # Debugging log content length

        response = HttpResponse(log_content, content_type='text/plain')
        response['Content-Disposition'] = 'attachment; filename=user_activity.log'
        return response
    except Exception as e:
        print(f"Error reading log file: {e}")
        return HttpResponse("Error reading log file.", status=500)

def filter_log_file(log_path, start_date, end_date, user, include_all_users):
    """Filter logs based on date and user"""
    filtered_logs = []
    print(f"Filtering log file at: {log_path}")

    if not os.path.exists(log_path):
        print(f"Log file not found at {log_path}")
        return "Log file not found."

    try:
        with open(log_path, 'r') as file:
            logs = file.readlines()
            print(f"Total logs read: {len(logs)}")

            for log in logs:
                print(f"Processing log line: {log.strip()}")
                parts = log.split(" ", 3)

                if len(parts) < 4:
                    print(f"Malformed log line: {log.strip()}")
                    continue  # Skip malformed lines
                
                log_date_str = parts[1]
                log_time_str = parts[2].split(",", 1)[0]  # Extract time without milliseconds
                log_message = parts[3]

                # Combine date and time for parsing
                try:
                    log_datetime = datetime.strptime(f"{log_date_str} {log_time_str}", "%Y-%m-%d %H:%M:%S")
                except ValueError as ve:
                    print(f"Date parsing error: {log_date_str} {log_time_str} ({ve})")
                    continue  # Skip lines that don't match the expected format

                # Debug output for filtered results
                print(f"Log datetime: {log_datetime}")
                print(f"Log message: {log_message}")

                # Filter by date and user
                if (not start_date or log_datetime >= datetime.strptime(start_date, "%Y-%m-%d")) and \
                   (not end_date or log_datetime <= datetime.strptime(end_date, "%Y-%m-%d")) and \
                   (include_all_users or (not user or user in log_message)):
                    filtered_logs.append(log)
                    print(f"Log added: {log.strip()}")

    except Exception as e:
        print(f"Error filtering log file: {e}")

    # Debug output for final results
    print(f"Filtered logs count: {len(filtered_logs)}")
    print("Filtered Logs:")
    print("\n".join(filtered_logs))
    
    return "\n".join(filtered_logs)
