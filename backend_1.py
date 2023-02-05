from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)

dict_all = {'jp': {'personal_normal_waiting': [2,4],
                   'personal_priority_waiting':[1,3],
                   'business_normal_waiting': [5,6,7,8],
                   'personal_skipped': [13,15],
                   'business_skipped': [24,56],
                   'current_queue_no': 0,
                   'current_assigned_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {},
                   'personal_normal_status': "",
                   'personal_priority_status': "",
                   'business_normal_status': "",
                   'system_status': "",
                   'avaliable_business_dict': {'p': 'Private Banking',
                  'b': 'Corporate Banking'},
                   'avaliable_priority_dict': {'y': 'Yes',
                  'n': 'No'}
                    },
            'je': {'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_assigned_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {},
                   'personal_normal_status': "",
                   'personal_priority_status': "",
                   'business_normal_status': "",
                   'system_status': "",
                   'avaliable_business_dict': {'p': 'Private Banking',
                  'b': 'Corporate Banking'},
                   'avaliable_priority_dict': {'y': 'Yes',
                  'n': 'No'}
                    },
            'kl':{'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_assigned_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {},
                   'personal_normal_status': "",
                   'personal_priority_status': "",
                   'business_normal_status': "",
                   'system_status': "",
                   'avaliable_business_dict': {'p': 'Private Banking',
                  'b': 'Corporate Banking'},
                   'avaliable_priority_dict': {'y': 'Yes',
                  'n': 'No'}
                    },
            'hg':{'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_assigned_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {},
                   'personal_normal_status': "",
                   'personal_priority_status': "",
                   'business_normal_status': "",
                   'system_status': "",
                   'avaliable_business_dict': {'p': 'Private Banking',
                  'b': 'Corporate Banking'},
                   'avaliable_priority_dict': {'y': 'Yes',
                  'n': 'No'}
                    }
            }

branch_dict = {'jp': 'Jurong Point',
               'je': 'Jurong East',
               'kl': 'Kuala Lumpur',
               'hg': 'Hou Gang'}
avaliable_branch_dict = {'jp': 'Jurong Point',
               'je': 'Jurong East',
               'kl': 'Kuala Lumpur',
               'hg': 'Hou Gang'}
business_dict = {'p': 'Private Banking',
                  'b': 'Corporate Banking'}
priority_dict = {'y': 'Yes',
                  'n': 'No'}
system_status_dict = {'a': 'Avaliable',
                       'l': 'Limited Functionality',
                       't': 'Terminated'}

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
  
# CRO add missed numbers function -Serena
def add_missed_num_to_queue(branch,type_of_business,priority,missednum):
    global dict_all
    personal_priority_waiting = dict_all[branch]['personal_priority_waiting']
    personal_normal_waiting = dict_all[branch]['personal_normal_waiting']
    business_normal_waiting = dict_all[branch]['business_normal_waiting']
    
    if type_of_business =='p' and priority == 'y':
        personal_priority_waiting.insert(2,missednum)
    elif type_of_business =='p' and priority == 'n':
        personal_normal_waiting.insert(2,missednum)
    elif type_of_business =='b':
        business_normal_waiting.insert(2,missednum)
    return missednum 
  

@app.route('/counter/<branch>/<type_of_business>/<counter>', methods=['GET', 'POST'])
def show1(branch, type_of_business, counter):
    global dict_all
    branch_name = branch_dict[branch]
    type_of_business_whole = business_dict[type_of_business]
    name = f"{branch_name} {type_of_business} {counter}"
    display_name = f"{type_of_business} {counter}"

    if request.form.get("button1"):
        button = request.form.get("button1")
    elif request.form.get("button2"):
        button = request.form.get("button2")
    elif request.form.get("button3"):
        button = request.form.get("button3")
    elif request.form.get("button4"):
        button = request.form.get("button4")

    current_queue_no = dict_all[branch]['current_queue_no']
    current_serving_personal = dict_all[branch]['current_serving_personal']
    current_serving_business = dict_all[branch]['current_serving_business']

    if request.method == 'POST' and button == "next" and type_of_business_whole == 'Private Banking':
        current_queue_no = get_next_personal_customer(branch)
        current_serving_personal[display_name] = current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == 'POST' and button == "next" and type_of_business_whole == 'Corporate Banking':
        current_queue_no = get_next_business_customer(branch)
        current_serving_business[display_name] = current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == "POST" and button == "skip" and type_of_business_whole == 'Private Banking':
        current_queue_no = skip_personal_customer(branch)
        current_serving_personal[display_name]= current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == "POST" and button == "skip" and type_of_business_whole == 'Corporate Banking':
        current_queue_no = skip_business_customer(branch)
        current_serving_business[display_name] = current_queue_no
        return render_template('counter_main.html', branch_name=branch_name, q=current_queue_no, counter=counter, type_of_business=type_of_business)

    elif request.method == 'POST' and button == 'stop':
        current_serving_business[display_name] = 'Stop Serving'
        return render_template('stop_serving.html', branch_name=branch_name, counter=counter, type_of_business=type_of_business)
    
    elif request.method == 'POST' and button == 'add_missed':
        return redirect(url_for('add_miss_num', branch=branch, type_of_business=type_of_business, counter=counter))
    
    return render_template('counter_main.html', branch_name=branch_name, q=None, counter=counter, type_of_business=type_of_business)


@app.route('/main_display/<branch>', methods=['GET','POST'])
def _show(branch):
    global dict_all
    current_serving_personal = dict_all[branch]['current_serving_personal']
    current_serving_business = dict_all[branch]['current_serving_business']
    personal_skipped = dict_all[branch]['personal_skipped']
    business_skipped = dict_all[branch]['business_skipped']
    system_status = dict_all[branch]['system_status']
    branch_name = branch_dict[branch]
    personal_normal_status = branch_dict[branch]['personal_normal_status']
    personal_priority_status = branch_dict[branch]['personal_priority_status']
    business_normal_status = branch_dict[branch]['business_normal_status']
    url = f"/main_display/" + branch
    return render_template('main_tv_display.html', current_serving_personal=current_serving_personal,
                           current_serving_business=current_serving_business,
                           personal_skipped = personal_skipped,
                           business_skipped = business_skipped,
                           system_status=system_status,
                           personal_normal_status=personal_normal_status,
                           personal_priority_status = personal_priority_status,
                           business_normal_status = business_normal_status,
                           url=url, branch_name=branch_name)

@app.route('/getq/mobile', methods=['GET','POST'])
def get_q_mobile():
    global dict_all

    if request.method == 'POST':
        type_of_business = request.form.get('type_of_business')
        priority = request.form.get('priority')
        branch = request.form.get('branch')
        checkstat = request.form.get("checkStat")

        if checkstat == "checkStat":
            return render_template('branch_status.html')
    
        if type_of_business is not None and priority is not None and branch is not None:
            current_assigned_queue_no = assign_queue_no_to_queue(branch, type_of_business, priority)
            type_of_business = business_dict[type_of_business]
            branch = branch_dict[branch]
            return render_template('queue_generated.html', q_number=current_assigned_queue_no, type_of_business=type_of_business, branch=branch)
        else:  #if user doesn't select all value, prompt user to input all required information
            return render_template('queue_gen_fail.html')
    return render_template('mobile_queue_gen.html', avaliable_branch_dict=avaliable_branch_dict, business_dict=business_dict, priority_dict=priority_dict)


@app.route('/getq/inperson/<branch>', methods=['GET','POST'])
def get_q_inperson(branch):
    global dict_all

    if dict_all[branch]['system_status'] == system_status_dict['t']:
        return render_template('service_terminated.html')

    if request.method == 'POST':
        type_of_business = request.form.get('type_of_business')
        priority = request.form.get('priority')
        if type_of_business == 'p' and priority == 'n':
            current_assigned_queue_no = assign_queue_no_to_queue(branch, type_of_business, priority)
            type_of_business = business_dict[type_of_business]
            branch_name = branch_dict[branch]
            waiting_numbers = dict_all[branch]['personal_normal_waiting']
            estimated_time = str(len(waiting_numbers*5))+'minutes'
            return render_template('queue_generated.html', q_number=current_assigned_queue_no, type_of_business=type_of_business, branch_name=branch_name, waiting_numbers=waiting_numbers, estimated_time=estimated_time)
        
        elif type_of_business == 'p' and priority == 'y':
            current_assigned_queue_no = assign_queue_no_to_queue(branch, type_of_business, priority)
            type_of_business = business_dict[type_of_business]
            branch_name = branch_dict[branch]
            waiting_numbers = dict_all[branch]['personal_priority_waiting']
            estimated_time = str(len(waiting_numbers*5))+'minutes'
            return render_template('queue_generated.html', q_number=current_assigned_queue_no, type_of_business=type_of_business, branch_name=branch_name, waiting_numbers=waiting_numbers, estimated_time=estimated_time)
        
        elif type_of_business == 'b':
            current_assigned_queue_no = assign_queue_no_to_queue(branch, type_of_business, priority)
            type_of_business = business_dict[type_of_business]
            branch_name = branch_dict[branch]
            waiting_numbers = len(dict_all[branch]['business_normal_waiting'])
            estimated_time = str(waiting_numbers*5)+'minutes'
            return render_template('queue_generated.html', q_number=current_assigned_queue_no, type_of_business=type_of_business, branch_name=branch_name, waiting_numbers=waiting_numbers, estimated_time=estimated_time)
        
        else:  #if user doesn't select all value, prompt user to input all required information
            return render_template('queue_gen_fail.html')
    branch_name = branch_dict[branch]
    avaliable_business_dict = dict_all[branch]['avaliable_business_dict']
    avaliable_priority_dict = dict_all[branch]['avaliable_priority_dict']
    return render_template('inperson_queue_gen.html', branch_dict=branch_dict, avaliable_business_dict=avaliable_business_dict, avaliable_priority_dict=avaliable_priority_dict, branch_name=branch_name)

@app.route('/cro/<branch>', methods=['GET','POST'])   #CRO Display, shows the queue status: serving, waiting, missed -Serena
def cro_show(branch):
    global dict_all
    global avaliable_branch_dict

    # For all buttons
    if request.form.get("button1"):
        button = request.form.get("button1")
    elif request.form.get("button2"):
        button = request.form.get("button2")
    elif request.form.get("button3"):
        button = request.form.get("button3")
    elif request.form.get("button4"):
        button = request.form.get("button4")
    elif request.form.get("button5"):
        button = request.form.get("button5")
    elif request.form.get("button6"):
        button = request.form.get("button6")
    elif request.form.get("button7"):
        button = request.form.get("button7")
        print('refreshed')
    elif request.form.get("button8"):
        button = request.form.get("button8")

    # buttons for changing either queue status
    if request.method == 'POST' and button == "terminatepn":
        dict_all[branch]['personal_normal_status'] = system_status_dict['t']
        dict_all[branch]['avaliable_priority_dict'].pop('n','This key does not exist') # Change avaliable business list of certain for mobile customer page
    if request.method == 'POST' and button == "reinitiatepn":
        dict_all[branch]['personal_normal_waiting'] = []
        dict_all[branch]['personal_normal_status'] = system_status_dict['a']
        dict_all[branch]['avaliable_priority_dict']['n'] = priority_dict['n'.format(branch=branch)] # Change avaliable branch list for mobile customer page

    if request.method == 'POST' and button == "terminatepp":
        dict_all[branch]['personal_priority_status'] = system_status_dict['t']
        dict_all[branch]['avaliable_priority_dict'].pop('y','This key does not exist') # Change avaliable business list of certain for mobile customer page
    if request.method == 'POST' and button == "reinitiatepp":
        dict_all[branch]['personal_priority_waiting'] = []
        dict_all[branch]['personal_priority_status'] = system_status_dict['a']
        dict_all[branch]['avaliable_priority_dict']['y'] = priority_dict['y'.format(branch=branch)] # Change avaliable branch list for mobile customer page

    if request.method == 'POST' and button == "terminatebn":
        dict_all[branch]['business_normal_status'] = system_status_dict['t']
        dict_all[branch]['avaliable_business_dict'].pop('b','This key does not exist') # Change avaliable business list of certain for mobile customer page
    if request.method == 'POST' and button == "reinitiatebn":
        dict_all[branch]['business_normal_waiting'] = []
        dict_all[branch]['business_normal_status'] = system_status_dict['a']
        dict_all[branch]['avaliable_business_dict']['b'] = business_dict['b'.format(branch=branch)] # Change avaliable branch list for mobile customer page
    
    # buttons for changing branch all queue status
    # coordinate queue status when changing all queue status
    if request.method == 'POST' and button == "terminateAll":
        dict_all[branch]['system_status'] = system_status_dict['t']
        avaliable_branch_dict.pop('{branch}'.format(branch=branch), 'This key does not exist') # Change avaliable branch list for mobile customer page

        dict_all[branch]['personal_normal_status'] = system_status_dict['t']
        dict_all[branch]['avaliable_priority_dict'].pop('n','This key does not exist') # Change avaliable business list of certain for mobile customer page
        
        dict_all[branch]['personal_priority_status'] = system_status_dict['t']
        dict_all[branch]['avaliable_priority_dict'].pop('y','This key does not exist') # Change avaliable business list of certain for mobile customer page

        dict_all[branch]['business_normal_status'] = system_status_dict['t']
        dict_all[branch]['avaliable_business_dict'].pop('b','This key does not exist') # Change avaliable business list of certain for mobile customer page

    if request.method == 'POST' and button == "reinitiateAll":
        dict_all[branch] = {'personal_normal_waiting': [],
                   'personal_priority_waiting':[],
                   'business_normal_waiting': [],
                   'personal_skipped': [],
                   'business_skipped': [],
                   'current_queue_no': 0,
                   'current_assigned_queue_no': 0,
                   'current_serving_personal': {},
                   'current_serving_business': {}
                    }
        dict_all[branch]['system_status'] = system_status_dict['a']
        avaliable_branch_dict['{branch}'] = branch_dict['{branch}'.format(branch=branch)] # Change avaliable branch list for mobile customer page
        
        dict_all[branch]['personal_normal_status'] = system_status_dict['a']
        dict_all[branch]['avaliable_priority_dict']['n'] = priority_dict['n'.format(branch=branch)] # Change avaliable branch list for mobile customer page
        
        dict_all[branch]['personal_priority_status'] = system_status_dict['a']
        dict_all[branch]['avaliable_priority_dict']['y'] = priority_dict['y'.format(branch=branch)] # Change avaliable branch list for mobile customer page
        
        dict_all[branch]['business_normal_status'] = system_status_dict['a']
        dict_all[branch]['avaliable_business_dict']['b'] = business_dict['b'.format(branch=branch)] # Change avaliable branch list for mobile customer page

    # coordinate system status when changing either queue status
    if dict_all[branch]['personal_normal_status'] == system_status_dict['a'] and dict_all[branch]['personal_priority_status'] == system_status_dict['a'] and dict_all[branch]['business_normal_status'] == system_status_dict['a']:
        dict_all[branch]['system_status'] = system_status_dict['a']
        avaliable_branch_dict['{branch}'] = branch_dict['{branch}'.format(branch=branch)] # Change avaliable branch list for mobile customer page
    elif dict_all[branch]['personal_normal_status'] == system_status_dict['t'] and dict_all[branch]['personal_priority_status'] == system_status_dict['t'] and dict_all[branch]['business_normal_status'] == system_status_dict['t']:
        dict_all[branch]['system_status'] = system_status_dict['t']
        avaliable_branch_dict.pop('{branch}'.format(branch=branch), 'This key does not exist') # Change avaliable branch list for mobile customer page
    else:
        dict_all[branch]['system_status'] = system_status_dict['l']
        avaliable_branch_dict['{branch}'] = branch_dict['{branch}'.format(branch=branch)] # Change avaliable branch list for mobile customer page

    if dict_all[branch]['personal_normal_status'] == system_status_dict['t'] and dict_all[branch]['personal_priority_status'] == system_status_dict['t']:
        dict_all[branch]['avaliable_business_dict'].pop('p','This key does not exist') # Change avaliable business list of certain for mobile customer page
    elif dict_all[branch]['personal_normal_status'] == system_status_dict['a'] or dict_all[branch]['personal_priority_status'] == system_status_dict['a']:
        dict_all[branch]['avaliable_business_dict']['p'] = business_dict['p'.format(branch=branch)] # Change avaliable branch list for mobile customer page

    current_serving_personal = dict_all[branch]['current_serving_personal']
    current_serving_business = dict_all[branch]['current_serving_business']
    personal_priority_waiting = dict_all[branch]['personal_priority_waiting']
    personal_normal_waiting = dict_all[branch]['personal_normal_waiting']
    business_normal_waiting = dict_all[branch]['business_normal_waiting']
    personal_skipped = dict_all[branch]['personal_skipped']
    business_skipped = dict_all[branch]['business_skipped']
    personal_normal_status = dict_all[branch]['personal_normal_status']
    personal_priority_status = dict_all[branch]['personal_priority_status']
    business_normal_status = dict_all[branch]['business_normal_status']
    system_status = dict_all[branch]['system_status']
    url = f"/cro/" + branch
    
    return render_template('cro_display.html', current_serving_personal= current_serving_personal,
                        current_serving_business=current_serving_business,
                        personal_priority_waiting=personal_priority_waiting,
                        personal_normal_waiting=personal_normal_waiting,
                        business_normal_waiting=business_normal_waiting,
                        personal_skipped=personal_skipped,
                        business_skipped=business_skipped,
                        system_status=system_status,
                        personal_normal_status=personal_normal_status,
                        personal_priority_status = personal_priority_status,
                        business_normal_status = business_normal_status,
                        url=url)

@app.route('/counter/<branch>/<type_of_business>/<counter>/manipulate', methods=['GET','POST']) #Counter Add missed numbers -Serena
def add_miss_num(branch, type_of_business, counter):
    global dict_all

    avaliable_business_dict = dict_all[branch]['avaliable_business_dict']
    avaliable_priority_dict = dict_all[branch]['avaliable_priority_dict']

    if request.method == 'POST':
        priority = request.form.get('priority')
        missednum = request.form.get('missednum')
        if type_of_business is not None and priority is not None:
            add_missed_num_to_queue(branch,type_of_business,priority,missednum)
            type_of_business = business_dict[type_of_business]
            branch = branch_dict[branch]
            return render_template('miss_added.html', missednum=missednum, type_of_business=type_of_business, branch=branch)
            
    return render_template('add_missed.html', avaliable_branch_dict=avaliable_branch_dict, avaliable_business_dict=avaliable_business_dict, avaliable_priority_dict=avaliable_priority_dict)

@app.route('/', methods=['GET','POST']) # Main Page for demonstration
def main():
    global dict_all

    # For buttons
    if request.form.get("button1"):
        button = request.form.get("button1")
    elif request.form.get("button2"):
        button = request.form.get("button2")
    elif request.form.get("button3"):
        button = request.form.get("button3")
    elif request.form.get("button4"):
        button = request.form.get("button4")
    elif request.form.get("button5"):
        button = request.form.get("button5")

    if request.method == 'POST' and button == "CROPage":
        return render_template('/cro/branches')
    if request.method == 'POST' and button == "QPage4Mobile":
        return redirect(url_for('/getq/mobile'))
    if request.method == 'POST' and button == "QPage4Inperson":
        return redirect(url_for('/getq/inperson/branches'))
    if request.method == 'POST' and button == "PublicDisplayPage":
        return render_template('/main_display/branches')
    if request.method == 'POST' and button == "CounterPage":
        return render_template('/counter/branches')
    return render_template('main_page.html', branch_dict=branch_dict, business_dict=business_dict, priority_dict=priority_dict)

@app.route('/test', methods=['GET','POST'])
def tester():
    return render_template('main_page.html')

if __name__ == '__main__':
    app.run(debug = True,port=8000)

