from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

dict_all = {'jp': {'personal_normal_waiting': [2,4],
                   'personal_priority_waiting':[3],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_assigned_queue_no': 0,
                   'current_serving_personal': {'personal 2':"2", 'personal 3':"3"},
                   'current_serving_business': {'business 1': "4", 'business 3': "5"}
                    },
            'je': {'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_assigned_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {}
                    },
            'kl':{'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                  'current_assigned_queue_no': 0,
                  'current_serving_personal': {},
                   'current_serving_business': {}
                    },
            'hg':{'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                  'current_assigned_queue_no': 0,
                  'current_serving_personal': {},
                   'current_serving_business': {}
                    }
            }

branch_dict = {'jp': 'Jurong Point',
               'je': 'Jurong East',
               'kl': 'Kuala Lumpur',
               'hg': 'Hou Gang'}
business_dict = {'p': 'Private Banking',
                  'b': 'Corporate Banking'}
priority_dict = {'y': 'Yes',
                  'n': 'No'}

def get_next_personal_customer(branch):
    """
    Get the queue number for the counter pressing 'NEXT' button.
    counter_id: denotes counter that press 'NEXT' button
    return current queue number
    """
    global dict_all
    personal_priority_waiting = dict_all[branch]['personal_priority_waiting']
    personal_normal_waiting = dict_all[branch]['personal_normal_waiting']
    current_queue_no = dict_all[branch]['current_queue_no']

    if not personal_priority_waiting:  # if personal_priority_waiting queue is empty, get queue number from personal_normal_waiting list
        if personal_normal_waiting:  # if personal_normal_waiting queue is not empty.
            current_queue_no = personal_normal_waiting[0]  # get the current queue number
            personal_normal_waiting.pop(0)  # Remove current_queue_no from personal_normal_waiting list
            return current_queue_no

        else:  # If personal_normal_waiting queue is empty
            return 'No customer in the queue'  # Prompt no customer notification to counter display screen

    if personal_priority_waiting:  # if personal_priority_waiting queue is not empty, get queue number from personal_priority_waiting list
        current_queue_no = personal_priority_waiting[0]
        personal_priority_waiting.pop(0)  # Remove current_queue_no from personal_priority_waiting list
        return current_queue_no


def get_next_business_customer(branch):
    global dict_all
    business_normal_waiting = dict_all[branch]['business_normal_waiting']
    current_queue_no = dict_all[branch]['current_queue_no']

    if business_normal_waiting:  # if business_normal_waiting queue is not empty.
        current_queue_no = business_normal_waiting[0]  # get the current queue number
        business_normal_waiting.pop(0)  # Remove current_queue_no from business_normal_waiting list
        return current_queue_no

    else:  # If business_normal_waiting queue is empty
        return 'No customer in the queue'  # Prompt no customer notification to counter display screen


def skip_personal_customer(branch):
    global dict_all
    current_queue_no = dict_all[branch]['current_queue_no']
    personal_skipped = dict_all[branch]['personal_skipped']
    if current_queue_no != 'No customer in the queue':
        personal_skipped.append(current_queue_no) # Append the skipped queue number to the personal_skipped list
        current_queue_no = get_next_personal_customer(branch)
        return current_queue_no
    else:
        return 'Cannot skip, no customer in the queue'


def skip_business_customer(branch):
    global dict_all
    current_queue_no = dict_all[branch]['current_queue_no']
    business_skipped = dict_all[branch]['business_skipped']

    if current_queue_no != 'No customer in the queue':
        business_skipped.append(current_queue_no) # Append the skipped queue number to the business_skipped list
        current_queue_no = get_next_business_customer(branch)
        return current_queue_no
    else:
        return 'Cannot skip, no customer in the queue'


def counter_name_parser(counter_id):
    branch_id = counter_id[:2]
    branch = branch_dict[branch_id]
    type_id = counter_id[3]
    type_of_business = business_dict[type_id]
    counterId = counter_id[5:]
    return branch, type_of_business, counterId, branch_id


def assign_queue_no_to_queue(branch, type_of_business, priority):
    global dict_all
    personal_priority_waiting = dict_all[branch]['personal_priority_waiting']
    personal_normal_waiting = dict_all[branch]['personal_normal_waiting']
    business_normal_waiting = dict_all[branch]['business_normal_waiting']
    current_assigned_queue_no = dict_all[branch]['current_assigned_queue_no']
    current_assigned_queue_no += 1
    dict_all[branch]['current_assigned_queue_no'] = current_assigned_queue_no

    if type_of_business =='p' and priority == 'y':
        personal_priority_waiting.append(current_assigned_queue_no)
    elif type_of_business =='p' and priority == 'n':
        personal_normal_waiting.append(current_assigned_queue_no)
    elif type_of_business =='b':
        business_normal_waiting.append(current_assigned_queue_no)
    return current_assigned_queue_no

@app.route('/counter/<branch>/<type_of_business>/<counter>', methods=['GET', 'POST'])
def show1(branch, type_of_business, counter):
    global dict_all
    branch_name = branch_dict[branch]
    type_of_business = business_dict[type_of_business]
    name = f"{branch_name} {type_of_business} {counter}"
    display_name = f"{type_of_business} {counter}"

    if request.form.get("button1"):
        button = request.form.get("button1")
    elif request.form.get("button2"):
        button = request.form.get("button2")
    elif request.form.get("button3"):
        button = request.form.get("button3")

    current_queue_no = dict_all[branch]['current_queue_no']
    current_serving_personal = dict_all[branch]['current_serving_personal']
    current_serving_business = dict_all[branch]['current_serving_business']

    if request.method == 'POST' and button == "next" and type_of_business == 'Private Banking':
        current_queue_no = get_next_personal_customer(branch)
        current_serving_personal[display_name] = current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == 'POST' and button == "next" and type_of_business == 'Corporate Banking':
        current_queue_no = get_next_business_customer(branch)
        current_serving_business[display_name] = current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == "POST" and button == "skip" and type_of_business == 'Private Banking':
        current_queue_no = skip_personal_customer(branch)
        current_serving_personal[display_name]= current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == "POST" and button == "skip" and type_of_business == 'Corporate Banking':
        current_queue_no = skip_business_customer(branch)
        current_serving_business[display_name] = current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == 'POST' and button == 'stop':
        current_serving_business[display_name] = 'Stop Serving'
        return render_template('stop_serving.html', branch_name=branch_name, counter=counter, type_of_business=type_of_business)

    return render_template('counter_main.html', branch_name=branch_name, q=None, counter=counter, type_of_business=type_of_business)


@app.route('/main_display/<branch>', methods=['GET','POST'])
def _show(branch):
    global dict_all
    current_serving_personal = dict_all[branch]['current_serving_personal']
    current_serving_business = dict_all[branch]['current_serving_business']
    url = f"/main_display/" + branch
    return render_template('main_tv_display.html', current_serving_personal=current_serving_personal,
                           current_serving_business=current_serving_business, url=url)


@app.route('/getq/mobile/<user>', methods=['GET','POST'])
def get_q_mobile(user):
    global dict_all

    if request.method == 'POST':
        type_of_business = request.form.get('type_of_business')
        priority = request.form.get('priority')
        branch = request.form.get('branch')

        if type_of_business is not None and priority is not None and branch is not None:
            current_assigned_queue_no = assign_queue_no_to_queue(branch, type_of_business, priority)
            type_of_business = business_dict[type_of_business]
            branch = branch_dict[branch]
            return render_template('queue_generated.html',user=user, q_number=current_assigned_queue_no, type_of_business=type_of_business, branch=branch)
        else:  #if user doesn't select all value, prompt user to input all required information
            return render_template('queue_gen_fail.html',user=user)
    return render_template('mobile_queue_gen.html', branch_dict=branch_dict, business_dict=business_dict, priority_dict=priority_dict)


@app.route('/getq/inperson/<branch>', methods=['GET','POST'])
def get_q_inperson(branch):
    global dict_all
    if request.method == 'POST':
        type_of_business = request.form.get('type_of_business')
        priority = request.form.get('priority')
        if type_of_business is not None and priority is not None:
            current_assigned_queue_no = assign_queue_no_to_queue(branch, type_of_business, priority)
            type_of_business = business_dict[type_of_business]
            branch = branch_dict[branch]
            return render_template('queue_generated.html', q_number=current_assigned_queue_no, type_of_business=type_of_business, branch=branch)
        else:  #if user doesn't select all value, prompt user to input all required information
            return render_template('queue_gen_fail.html')

    return render_template('inperson_queue_gen.html', branch_dict=branch_dict, business_dict=business_dict, priority_dict=priority_dict)


if __name__ == '__main__':
    app.run(debug = True,port=8000)

