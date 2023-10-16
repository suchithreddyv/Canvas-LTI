from django.http import HttpResponse
from django.shortcuts import render
import requests

# Create your views here.
def index(request):
    api_url = "https://canvas.instructure.com/api/v1/"

    # Authentication headers (replace with your API token or OAuth)
    headers = {
        "Authorization": "Bearer 7~ydK6n6TKAKDz0BkWVbIdjwUt5xduU2qumD4tVriKKscd4xiN5VLI4vb5l9H403mT"
    }

    # Course ID (replace with the specific course ID you want to retrieve users from)
    course_id = request.POST["custom_course_id"]
    course_name =  request.POST["custom_course_name"]

    # Roles you want to filter
    roles = ["student"]

    # Make the API call
    response = requests.get(f"{api_url}courses/{course_id}/users", headers=headers, params={"enrollment_type[]": roles})

    print(response.content)

    if response.status_code == 200:
        users_data = response.json()
        user_list = [(user['id'], user['name']) for user in users_data]
        assignments_data = []
        
        # Make the API call to retrieve assignments
        response_assignments = requests.get(f"{api_url}courses/{course_id}/assignments", headers=headers)
        
        if response_assignments.status_code == 200:
            assignments_data = response_assignments.json()
        
        result = []
        
        # Iterate through users
        for user_id, user_name in user_list:
            user_assignments = []
            
            # Iterate through assignments for each user
            for assignment in assignments_data:
                assignment_id = assignment['id']
                submission_url = f"{api_url}courses/{course_id}/assignments/{assignment_id}/submissions/{user_id}"
                response_submission = requests.get(submission_url, headers=headers)
                if response_submission.status_code == 200:
                    submission_data = response_submission.json()
                    submitted = submission_data.get('workflow_state') == 'submitted'
                else:
                    submitted = False
                
                user_assignments.append({
                    'Assignment Name': assignment['name'],
                    'Submission Status': submitted
                })
            
            result.append({
                'Student Name': user_name,
                'Assignments': user_assignments
            })
        
        response_text = f"List of Users and Their Assignment Status for Course {course_name}:\n\n"
        for user in result:
            user_name = user.get('Student Name', 'Name not available')  # Use a default if user_name is missing
            response_text += f"Student Name: {user_name}\n"
            response_text += "Assignments:\n"
            for assignment in user.get('Assignments', []):  # Use an empty list if assignments are missing
                assignment_name = assignment.get('Assignment Name', 'Name not available')  # Use a default if assignment_name is missing
                submitted_status = 'Submitted' if assignment.get('Submission Status', False) else 'Not Submitted'
                response_text += f"  - Assignment Name: {assignment_name}\n"
                response_text += f"    Submission Status: {submitted_status}\n\n"

        return HttpResponse(response_text, content_type="text/plain")
    
    return HttpResponse("API call failed with status code: " + str(response.status_code))
