from flask import Flask
from flask import request, jsonify
from models import Scheduling, db, User
from app import application
import datetime
      
#List a specific company’s working hours

@application.route('/company_hours', methods=['POST'])
def company_hours():
    data = request.get_json()
    hours = Scheduling.query.filter_by(company_id=data['company_id']).all()
    
    output = []
    
    for hour in hours:
        hour_data = {}
        hour_data['id'] = hour.id
        hour_data['company'] = hour.company.name
        hour_data['client'] = hour.client.name
        hour_data['title'] = hour.title
        hour_data['start_time'] = hour.start_time
        hour_data['end_time'] = hour.end_time
        # hour_data['total_hours'] = pass
        
        output.append(hour_data)
        
    return jsonify({'company_hours': output}), 200

#List all schedulings
@application.route('/schedulings', methods=['GET'])
def schedulings():
    all_schedulings = Scheduling.query.all()
    
    output = []
    
    for scheduling in all_schedulings:
        scheduling_data = {}
        scheduling_data['id'] = scheduling.id
        scheduling_data['title'] = scheduling.title
        scheduling_data['company_id'] = scheduling.company_id
        scheduling_data['company'] = scheduling.company.name
        scheduling_data['client_id'] = scheduling.client_id
        scheduling_data['client'] = scheduling.client.name
        scheduling_data['start_time'] = scheduling.start_time
        scheduling_data['end_time'] = scheduling.end_time
        scheduling_data['is_active'] = scheduling.is_active
        output.append(scheduling_data)        
    return jsonify({'schedulings': output}), 200

#Make, cancel, edit, view scheduling

@application.route('/scheduling', methods=['GET', 'POST', 'PUT', 'DELETE'])
def scheduling_cruds():
    if request.method == 'GET':
        all_schedulings = Scheduling.query.all()
    
        output = []
        
        for scheduling in all_schedulings:
            scheduling_data = {}
            scheduling_data['id'] = scheduling.id
            scheduling_data['title'] = scheduling.title
            scheduling_data['company_id'] = scheduling.company_id
            scheduling_data['company'] = scheduling.company.name
            scheduling_data['client_id'] = scheduling.client_id
            scheduling_data['client'] = scheduling.client.name
            scheduling_data['start_time'] = scheduling.start_time
            scheduling_data['end_time'] = scheduling.end_time
            scheduling_data['is_active'] = scheduling.is_active
            output.append(scheduling_data)
            
        return jsonify({'schedulings': output}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        #Convert string time to python datetime
        start_time = datetime.strptime(data['start_time'], '%d/%m/%y %H:%M')
        end_time = datetime.strptime(data['end_time'], '%d/%m/%y %H:%M')
        
        #Check if slot is available
        times = Scheduling.query.filter_by(is_active=True).all()
        
        # Get session duration
        initial_duration = User.query.filter_by(id=data['company_id']).first().session_duration
        
        for time in times:
            diff = end_time - start_time
            
            #difference in minutes
            diff = diff.total_seconds() / 60
            
            #duration in minutes
            duration = int(initial_duration) * 60
            
            #Cast to integer
            diff = int(diff)
            duration = int(duration)
            
            if diff != duration:
                return jsonify({'msg': f'Session duration should be {initial_duration} hours'}), 401
            
            if start_time >= time.start_time and end_time <= time.end_time:
                return jsonify({'msg': 'Scheduling not successfully, that session is already booked'}), 401
            
        add_scheduling = Scheduling(title=data['title'], company_id=data['company_id'], client_id=data['client_id'], start_time=start_time, end_time=end_time, is_active=True)
        db.session.add(add_scheduling)
        db.session.commit()
        
        return jsonify({'msg': 'Scheduling added successfully'}), 201
    
    elif request.method == 'POST':
        data = request.get_json()
        
        scheduling = Scheduling.query.filter_by(id=data['id'])#.first()
        
        if data['title']:
            scheduling.update({'title':data['title']})
            db.session.commit()
            return jsonify({'msg':'Title updated successfully'}), 200
        
        elif data['company_id']:
            scheduling.update({'company_id':data['company_id']})
            db.session.commit()
            return jsonify({'msg':'Company updated successfully'}), 200
        
        elif data['client_id']:
            scheduling.update({'client_id':data['client_id']})
            db.session.commit()
            return jsonify({'msg':'Client updated successfully'}), 200
        
        elif data['start_time']:
            scheduling.update({'start_time':datetime.strptime(data['start_time'], '%d/%m/%y %H:%M')})
            db.session.commit()
            return jsonify({'msg':'Start time updated successfully'}), 200
        
        elif data['end_time']:
            scheduling.update({'end_time':datetime.strptime(data['end_time'], '%d/%m/%y %H:%M')})
            db.session.commit()
            return jsonify({'msg':'End time updated successfully'}), 200
        
        else:
            return jsonify({'msg':'Wrong parameter'}), 401
        
    elif request.method == 'DELETE':
        #Soft Delete
        data = request.get_json()
        
        scheduling = Scheduling.query.filter_by(id=data['id']).update(dict(is_active=False))
        db.session.commit()
        
        return jsonify({'msg':'Scheduling cancelled successfully'}), 200
    
    else:
        return jsonify({'msg':'Wrong method'}), 401
