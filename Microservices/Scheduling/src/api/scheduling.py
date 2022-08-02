from flask import Flask
from flask import request, jsonify
from models import *
from main import application
      
#List a specific company’s working hours

@application.route('/company_hours', methods=['POST'])
def company_hours():
    data = request.get_json()
    hours = Appointment.query.filter_by(company_id=data['company_id']).all()
    
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

#List all appointments
@application.route('/appointments', methods=['GET'])
def appointments():
    all_appointments = Appointment.query.all()
    
    output = []
    
    for appointment in all_appointments:
        appointment_data = {}
        appointment_data['id'] = appointment.id
        appointment_data['title'] = appointment.title
        appointment_data['company_id'] = appointment.company_id
        appointment_data['company'] = appointment.company.name
        appointment_data['client_id'] = appointment.client_id
        appointment_data['client'] = appointment.client.name
        appointment_data['start_time'] = appointment.start_time
        appointment_data['end_time'] = appointment.end_time
        appointment_data['is_active'] = appointment.is_active
        output.append(appointment_data)        
    return jsonify({'appointments': output}), 200

#Make, cancel, edit, view appointment

@application.route('/appointment', methods=['GET', 'POST', 'PUT', 'DELETE'])
def appointment_cruds():
    if request.method == 'GET':
        all_appointments = Appointment.query.all()
    
        output = []
        
        for appointment in all_appointments:
            appointment_data = {}
            appointment_data['id'] = appointment.id
            appointment_data['title'] = appointment.title
            appointment_data['company_id'] = appointment.company_id
            appointment_data['company'] = appointment.company.name
            appointment_data['client_id'] = appointment.client_id
            appointment_data['client'] = appointment.client.name
            appointment_data['start_time'] = appointment.start_time
            appointment_data['end_time'] = appointment.end_time
            appointment_data['is_active'] = appointment.is_active
            output.append(appointment_data)
            
        return jsonify({'appointments': output}), 200
    
    elif request.method == 'PUT':
        data = request.get_json()
        
        #Convert string time to python datetime
        start_time = datetime.strptime(data['start_time'], '%d/%m/%y %H:%M')
        end_time = datetime.strptime(data['end_time'], '%d/%m/%y %H:%M')
        
        #Check if slot is available
        times = Appointment.query.filter_by(is_active=True).all()
        
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
                return jsonify({'msg': 'Appointment not successfully, that session is already booked'}), 401
            
        add_appointment = Appointment(title=data['title'], company_id=data['company_id'], client_id=data['client_id'], start_time=start_time, end_time=end_time, is_active=True)
        db.session.add(add_appointment)
        db.session.commit()
        
        return jsonify({'msg': 'Appointment added successfully'}), 201
    
    elif request.method == 'POST':
        data = request.get_json()
        
        appointment = Appointment.query.filter_by(id=data['id'])#.first()
        
        if data['title']:
            appointment.update({'title':data['title']})
            db.session.commit()
            return jsonify({'msg':'Title updated successfully'}), 200
        
        elif data['company_id']:
            appointment.update({'company_id':data['company_id']})
            db.session.commit()
            return jsonify({'msg':'Company updated successfully'}), 200
        
        elif data['client_id']:
            appointment.update({'client_id':data['client_id']})
            db.session.commit()
            return jsonify({'msg':'Client updated successfully'}), 200
        
        elif data['start_time']:
            appointment.update({'start_time':datetime.strptime(data['start_time'], '%d/%m/%y %H:%M')})
            db.session.commit()
            return jsonify({'msg':'Start time updated successfully'}), 200
        
        elif data['end_time']:
            appointment.update({'end_time':datetime.strptime(data['end_time'], '%d/%m/%y %H:%M')})
            db.session.commit()
            return jsonify({'msg':'End time updated successfully'}), 200
        
        else:
            return jsonify({'msg':'Wrong parameter'}), 401
        
    elif request.method == 'DELETE':
        #Soft Delete
        data = request.get_json()
        
        appointment = Appointment.query.filter_by(id=data['id']).update(dict(is_active=False))
        db.session.commit()
        
        return jsonify({'msg':'Appointment cancelled successfully'}), 200
    
    else:
        return jsonify({'msg':'Wrong method'}), 401
