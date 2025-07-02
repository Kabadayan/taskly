from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
import json
from .forms import TaskForm
from .models import Task
import uuid

def index_page(request):
    """
    Renders the main HTML page with an empty task form.
    This view serves the frontend page for task creation.
    """
    form = TaskForm()
    return render(request, 'todo/index.html', {'form': form})

def index_view(request):
    """
    Returns a JSON response containing the user's incomplete tasks.
    If the user is authenticated, tasks are fetched from the database.
    If not authenticated, tasks are retrieved from the session.
    """
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user, is_completed=False).values('id', 'name', 'is_completed')
        tasks_list = list(tasks)
    else:
        tasks_list = [t for t in request.session.get('tasks', []) if not t.get('is_completed')]
    return JsonResponse({'tasks': tasks_list})

def create_task(request):
    """
    Handles task creation via POST request.
    - Validates JSON and form input.
    - Saves the task to the database (if user is logged in).
    - Stores the task in session (if user is anonymous).
    Returns a JSON response indicating success or error.
    """
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except Exception:
            return JsonResponse({'errors': 'Invalid JSON'}, status=400)

        form = TaskForm(data)
        if form.is_valid():
            if request.user.is_authenticated:
                task = form.save(commit=False)
                task.user = request.user
                task.save()
            else:
                task_data = form.cleaned_data
                task_data['id'] = str(uuid.uuid4())
                task_data['is_completed'] = False
                session_tasks = request.session.get('tasks', [])
                session_tasks.append(task_data)
                request.session['tasks'] = session_tasks

            return JsonResponse({'message': 'Task created successfully'})
        else:
            return JsonResponse({'errors': form.errors}, status=400)
    else:
        return JsonResponse({'error': 'Only POST allowed'}, status=405)

def update_task(request, task_id):
    """
    Handles task updates via PUT request.
    - If the user is authenticated, updates the database task.
    - If anonymous, updates the corresponding task in session.
    Valid fields to update: 'name' and 'is_completed'.
    Returns a JSON response indicating result.
    """
    if request.method != "PUT":
        return JsonResponse({'error': 'Method not allowed'}, status=405)

    try:
        # For authenticated users, task_id is expected to be an integer (database ID).
        task_id_int = int(task_id)
        task = get_object_or_404(Task, id=task_id_int, user=request.user)

        data = json.loads(request.body)
        updated = False

        if 'name' in data:
            task.name = data['name']
            updated = True
        if 'is_completed' in data:
            task.is_completed = data['is_completed']
            updated = True

        if updated:
            task.save()
            return JsonResponse({'message': 'Task updated successfully'})
        else:
            return JsonResponse({'error': 'No valid fields to update'}, status=400)

    except ValueError:
        # For anonymous users, task_id is a UUID (string), and tasks are stored in session.
        session_tasks = request.session.get('tasks', [])
        task = next((t for t in session_tasks if t['id'] == task_id), None)

        if not task:
            return JsonResponse({'error': 'Task not found in session'}, status=404)

        data = json.loads(request.body)
        updated = False

        if 'name' in data:
            task['name'] = data['name']
            updated = True
        if 'is_completed' in data:
            task['is_completed'] = data['is_completed']
            updated = True

        if updated:
            # Update the task in the session task list
            for i, t in enumerate(session_tasks):
                if t['id'] == task_id:
                    session_tasks[i] = task
                    break
            request.session['tasks'] = session_tasks
            return JsonResponse({'message': 'Task updated successfully'})
        else:
            return JsonResponse({'error': 'No valid fields to update'}, status=400)

def delete_task(request, task_id):
    """
    Handles task deletion via DELETE request.
    - For authenticated users, deletes the task from the database.
    - For anonymous users, removes the task from the session.
    Returns a JSON response confirming deletion.
    """
    if request.method != "DELETE":
        return JsonResponse({'error': 'Invalid method'}, status=405)

    try:
        # Try to parse task_id as integer (database ID)
        task_id_int = int(task_id)
        task = get_object_or_404(Task, id=task_id_int, user=request.user)
        task.delete()
        return JsonResponse({'message': 'Task deleted'})
    except ValueError:
        # If task_id is a UUID (for anonymous users), remove from session
        session_tasks = request.session.get('tasks', [])
        session_tasks = [t for t in session_tasks if t['id'] != task_id]
        request.session['tasks'] = session_tasks
        return JsonResponse({'message': 'Session task deleted'})