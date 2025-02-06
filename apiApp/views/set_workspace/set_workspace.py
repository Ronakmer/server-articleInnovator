
from django.contrib import messages
from django.shortcuts import render,redirect
from apiApp.models import workspace, user_detail
from django.http import HttpResponse,HttpResponseRedirect,JsonResponse


def set_workspace(request):
    try:
        # Fetch the workspace based on the ID from the POST request
        workspace_slug_id = request.POST.get('workspace_slug_id')
        selected_workspace = workspace.objects.filter(slug_id = workspace_slug_id).first()

        print(selected_workspace,'98458')
        if selected_workspace:
            # Store the required workspace details in the session
            request.session['workspace'] = {
                'id': selected_workspace.id,
                'slug_id': selected_workspace.slug_id,
                'name': selected_workspace.name,
                'logo': selected_workspace.logo.url if selected_workspace.logo else ''
            }
        else:
            # Clear the workspace session data if no workspace is found
            request.session['workspace'] = None
        
    except Exception as e:
        print("This error is set_workspace --->: ", e)
        return render(request, 'error.html', {'error': 500})