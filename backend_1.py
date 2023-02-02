from flask import Flask, render_template, request
app = Flask(__name__)

dict_all = {'jp': {'personal_normal_waiting': [2,4],
                   'personal_priority_waiting':[3],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_serving_personal': {'personal 2':6, 'personal 3':2},
                   'current_serving_business': {'business 1': 2, 'business 3': 3}
                    },
            'je': {'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {}
                    },
            'kl':{'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {}
                    },
            'hg':{'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {}
                    }
            }

branch_dict = {'jp': 'Jurong Point',
               'je': 'Jurong East',
               'kl': 'Kuala Lumpur',
               'hg': 'Hou Gang'}
business_dict = {'p': 'personal',
                 'b': 'business'}

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

def add_personal_normal_waiting(branch):
    pass

def add_business_normal_waiting(branch):
    pass

def add_personal_priority_waiting(branch):
    pass

@app.route('/counter/<counter_id>', methods=['GET', 'POST'])
def __show(counter_id):
    global dict_all
    branch_name, type_of_business, counterId, branch = counter_name_parser(counter_id)
    name = f"{branch_name} {type_of_business} {counterId}"
    display_name = f"{type_of_business} {counterId}"
    button = request.form.get("button1") if request.form.get("button1") else request.form.get("button2")

    current_queue_no = dict_all[branch]['current_queue_no']
    current_serving_personal = dict_all[branch]['current_serving_personal']
    current_serving_business = dict_all[branch]['current_serving_business']

    if request.method == 'POST' and button == "next" and type_of_business == 'personal':
        current_queue_no = get_next_personal_customer(branch)
        current_serving_personal[display_name] = current_queue_no
        return render_template('counter_page_1.html', counterName=name, q=current_queue_no)

    elif request.method == 'POST' and button == "next" and type_of_business == 'business':
        current_queue_no = get_next_business_customer(branch)
        current_serving_business[display_name] = current_queue_no
        return render_template('counter_page_1.html', counterName=name, q=current_queue_no)

    elif request.method == "POST" and button == "skip" and type_of_business == 'personal':
        current_queue_no = skip_personal_customer(branch)
        current_serving_personal[display_name]= current_queue_no
        return render_template('counter_page_1.html', counterName=name, q=current_queue_no)

    elif request.method == "POST" and button == "skip" and type_of_business == 'business':
        current_queue_no = skip_business_customer(branch)
        current_serving_business[display_name] = current_queue_no
        return render_template('counter_page_1.html', counterName=name, q=current_queue_no)

    return render_template('counter_page_1.html', counterName=name, q=None)


@app.route('/main_display/<branch>', methods=['GET','POST'])
def _show(branch):
    global dict_all
    current_serving_personal = dict_all[branch]['current_serving_personal']
    current_serving_business = dict_all[branch]['current_serving_business']
    url = f"/main_display/" + branch
    return render_template('main_display.html', current_serving_personal=current_serving_personal,
                           current_serving_business=current_serving_business, url=url)


@app.route('/customer_get_queue/mobile', methods=['GET','POST'])
def get_q_mobile():
    return render_template('queue.html', branch_dict=branch_dict, business_dict=business_dict)


if __name__ == '__main__':
    app.run(debug = True,port=8080)

