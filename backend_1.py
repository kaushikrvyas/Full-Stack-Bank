from flask import Flask, render_template, request
app = Flask(__name__)

personal_normal_waiting = [2,4,5]
personal_priority_waiting = [3]
business_normal_waiting = [1,2,3]
personal_skipped = []
business_skipped = []
current_queue_no = 1

def get_next_personal_customer():
    """
    Get the queue number for the counter pressing 'NEXT' button.
    counter_id: denotes counter that press 'NEXT' button
    return current queue number
    """
    global current_queue_no
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


def get_next_business_customer():
    global current_queue_no
    if not business_skipped:  # if business_skipped queue is empty, get queue number from business_normal_waiting list
        if business_normal_waiting:  # if business_normal_waiting queue is not empty.
            current_queue_no = business_normal_waiting[0]  # get the current queue number
            business_normal_waiting.pop(0)  # Remove current_queue_no from business_normal_waiting list
            return current_queue_no

        else:  # If business_normal_waiting queue is empty
            return 'No customer in the queue'  # Prompt no customer notification to counter display screen


def skip_personal_customer():
    global current_queue_no
    global personal_skipped

    if current_queue_no != 'No customer in the queue':
        personal_skipped.append(current_queue_no) # Append the skipped queue number to the personal_skipped list
        current_queue_no = get_next_personal_customer()
        return current_queue_no
    else:
        return 'Cannot skip, no customer in the queue'

def skip_business_customer():
    global current_queue_no
    global personal_skipped

    if current_queue_no != 'No customer in the queue':
        business_skipped.append(current_queue_no) # Append the skipped queue number to the business_skipped list
        current_queue_no = get_next_business_customer()
        return current_queue_no
    else:
        return 'Cannot skip, no customer in the queue'


@app.route('/counter/jp_p_2', methods=['GET','POST'])
def next():

    button = request.form.get("button1") if request.form.get("button1") else request.form.get("button2")
    if request.method == 'POST' and button == "next":
        current_queue_no = get_next_personal_customer()
        return render_template('counter_page_jp_p_2.html', q=current_queue_no)
    elif request.method == "POST" and button == "skip":
        current_queue_no = skip_personal_customer()
        return render_template('counter_page_jp_p_2.html', q=current_queue_no)
    return render_template('counter_page_jp_p_2.html', q=None)


@app.route('/counter/jp_b_1', methods=['GET','POST'])
def next2():

    button = request.form.get("button1") if request.form.get("button1") else request.form.get("button2")
    if request.method == 'POST' and button == "next":
        current_queue_no = get_next_business_customer()
        return render_template('counter_page_jp_b_1.html', q=current_queue_no)
    elif request.method == "POST" and button == "skip":
        current_queue_no = skip_business_customer()
        return render_template('counter_page_jp_b_1.html', q=current_queue_no)
    return render_template('counter_page_jp_b_1.html', q=None)


if __name__ == '__main__':
    app.run(host = "localhost",debug = True,port=8080)


