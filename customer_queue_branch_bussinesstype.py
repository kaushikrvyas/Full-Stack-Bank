from flask import Flask, request, render_template

app = Flask(__name__)

# Store the customer queue numbers for each branch and business type
queue = []

@app.route("....route api here......", methods=["GET", "POST"])
def add_customer():
    if request.method == "POST":
        # Get the customer details from the request
        branch = request.form.get("branch")
        business_type = request.form.get("business_type")
        customer_name = request.form.get("customer_name")
        
        # Add the customer to the end of the queue
        queue.append({"branch": branch, "business_type": business_type, "customer_name": customer_name})
        
        return "Customer added to queue successfully!"
    else:
        return render_template(".......insert customer add html here...")

@app.route("...route api here....", methods=["GET"])
def get_queue():
    # Get the branch and business type from the request
    branch = request.args.get("branch")
    business_type = request.args.get("business_type")
    
    # Get the customer queue for the given branch and business type
    customer_queue = [c for c in queue if c["branch"] == branch and c["business_type"] == business_type]
    
    return "Queue for {}-{}: {}".format(branch, business_type, customer_queue)

if __name__ == "__main__":
    app.run()
