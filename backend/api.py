import os
from flask import Flask
from flask import request
from supabase_client import supabase
from dotenv import load_dotenv
from NER.main import pdf_to_text, extract_assignments, extract_class_location, extract_class_title
from calendar_service import CalendarService

load_dotenv()
app = Flask(__name__)


@app.route('/api/calendar', methods=['POST'])
def load_calendar():
  data = request.get_json()
  token = data.get('token')
  file_path = data.get('file_path')

  service = CalendarService(token)
  
  def get_relative_path(full_url):
    return full_url.split("/public/pdfs/", 1)[1]

  file_name = "temp_pdf.pdf"
  try:
    with open(file_name, "wb") as f:
      response = supabase.storage.from_("pdfs").download(get_relative_path(file_path))
      f.write(response)
    # call pdf to text function here

    text = pdf_to_text(file_name)
    calendar_data = parse_info(text)
    response = service.add_to_calendar(calendar_data)

    if not response:
      raise Exception("Unable to add to calendar")

    # delete pdf here
    os.remove(file_name)

    return {
      "message": "Successfully added to calendar",
      "successfully_added_events": response
    }, 200

  except FileNotFoundError:
    return {"error": str(e)}, 500
  except Exception as e:
    return {"error": str(e)}, 500
  
def parse_info(text):

  assignments = extract_assignments(text)
  location = extract_class_location(text)
  class_name = extract_class_title(text)
  
  
  if not assignments:
    raise Exception("Assignments not found")
  if not location:
    raise Exception("Location not found")
  if not class_name:
    raise Exception("Class name is not found")

  dict = {}

  dict["assignments"] = assignments
  dict["location"] = location
  dict["class_name"] = class_name

  return dict 

@app.route('/api/task', methods=['GET', 'POST', 'DELETE', 'PUT'])
def task():
    data = request.get_json()

    token = data.get('token')
    service = CalendarService(token) if token else None
    user_id = data.get('user_id')
    task_id = data.get('task_id')

    if request.method == 'POST':
        course_id = data.get('course_id')
        name = data.get('name')
        if not all([user_id, course_id, name]):
            return "Non-null fields are missing", 400
        
        return create_task(
            user_id=user_id,
            course_id=course_id,
            name=name,
            type=data.get('type'),
            is_completed=data.get('is_completed'),
            due_date=data.get('due_date'),
            note=data.get('note'),
            calendar_link=data.get('calendar_link'),
            calendar_service=service
        )

    elif request.method == 'PUT':
        name = data.get('name')
        if not all([user_id, task_id, name]):
            return "Non-null fields are missing", 400
        
        return update_task(
            user_id=user_id,
            task_id=task_id,
            name=name,
            type=data.get('type'),
            is_completed=data.get('is_completed'),
            due_date=data.get('due_date'),
            note=data.get('note'),
            calendar_link=data.get('calendar_link'),
            calendar_service=service
        )

    elif request.method == 'GET':
        if not user_id:
            return {"error": "No user id specified"}, 400
        return get_tasks(user_id, task_id)

    elif request.method == 'DELETE':
        if not all([user_id, task_id]):
            return {"error": "No task id or user id specified"}, 400
        return delete_task(user_id, task_id, calendar_service=service)


def create_task(user_id, course_id=None, name=None, type=None, is_completed=None, due_date=None, note=None, calendar_link=None, calendar_service=None):
  try:
    response = (
      supabase.table("task")
      .insert({
        "user_id": user_id,
        "course_id": course_id,
        "name": name,
        "type": type,
        "is_completed": is_completed,
        "due_date": due_date,
        "note": note,
        "calendar_link": calendar_link
      })
      .execute()
    )
    if not response.data:
      return {"message": "Couldn't create task"}, 404
    
    created_task = response.data[0]
    task_id = created_task["task_id"]
    
    if calendar_service and due_date:
      
      # FAILING HERE
      created_event = calendar_service.create_event(
        summary=name,
        description=note,
        due_date=due_date
      )
      if created_event:
        event_id = created_event.get("id")
        link = created_event.get("htmlLink")

        update_data = {
          "calendar_event_id": event_id,
          "calendar_link": link
        }
        supabase.table("task").update(update_data).eq("task_id", task_id).execute()

        created_task["calendar_event_id"] = event_id
        created_task["calendar_link"] = link

    return created_task, 200
    
  except Exception as e:
    return {"error": str(e)}, 500

def update_task(user_id, task_id, name=None, type=None, is_completed=None, due_date=None, note=None, calendar_link=None, calendar_service=None):
  try:

    existing_task = (
      supabase.table('task')
      .select('*')
      .eq('task_id', task_id)
      .eq('user_id', user_id)
      .single()
      .execute()
    )
    
    if not existing_task.data:
      return {"message": "No tasks found to update"}, 404

    existing_task = existing_task.data
    old_event_id = existing_task.get("calendar_event_id")
      
    
    fields_to_update = {}
    if name is not None:
      fields_to_update["name"] = name
    if type is not None:
      fields_to_update["type"] = type
    if is_completed is not None:
      fields_to_update["is_completed"] = is_completed
    if due_date is not None:
      fields_to_update["due_date"] = due_date
    if note is not None:
      fields_to_update["note"] = note
    
    if calendar_service:
      if old_event_id:
          updated_event = calendar_service.update_event(
            event_id=old_event_id,
            summary=name,
            description=note,
            due_date=due_date
          )
          if updated_event:
            fields_to_update["calendar_link"] = updated_event["htmlLink"]
            fields_to_update["calendar_event_id"] = updated_event["id"]
      else:
          if due_date:
            created_event = calendar_service.create_event(
              summary=name,
              description=note,
              due_date=due_date
            )
            if created_event:
              fields_to_update["calendar_link"] = created_event["htmlLink"]
              fields_to_update["calendar_event_id"] = created_event["id"]

    update_resp = (
        supabase.table("task")
        .update(fields_to_update)
        .eq("task_id", task_id)
        .execute()
    )
    if not update_resp.data:
        return {"message": "No tasks found after update"}, 404

    return update_resp.data, 200
    
  except Exception as e:
    return {"error": str(e)}, 500


def get_tasks(user_id, task_id):
  try:
    query = supabase.table("task").select("*")

    if user_id:
        query = query.eq("user_id", user_id)
    
    if task_id:
        query = query.eq("task_id", task_id)
    
    response = query.execute()
    if not response.data:
        return {"message": "No tasks found"}, 404
    return response.data, 200
  except Exception as e:
    return {"error": str(e)}, 500

    
def delete_task(user_id, task_id, calendar_service=None):
  try:
    existing_task_resp = (
      supabase.table("task")
      .select("*")
      .eq("task_id", task_id)
      .eq("user_id", user_id)
      .single()
      .execute()
    )

    if not existing_task_resp.data:
      return {"message": f"No task found with id {task_id}"}, 404

    existing_task = existing_task_resp.data
    event_id = existing_task.get("calendar_event_id")

    if calendar_service and event_id:
      calendar_service.delete_event(event_id)
    response = (
      supabase
      .table("task")
      .delete()
      .eq("task_id", task_id)
      .eq("user_id", user_id)
      .execute()
    )
    if response.count == 0:
      return {"message": f"No task found with id {task_id}"}, 404

    return {"message": f"Task {task_id} deleted"}, 200
  except Exception as e:
    return {"error": str(e)}, 500

    
 
     