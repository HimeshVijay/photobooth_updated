from flask import Flask, render_template_string, request
import razorpay
import subprocess
import webbrowser
import os

app = Flask(__name__)

# Razorpay test keys (replace with your secret)
razorpay_client = razorpay.Client(auth=("rzp_test_R8Pjr1V054idbz", "mifvbSWk8SLhiOdejqOCRyeZ"))

# Inline HTML template
html_template = """
<!doctype html>
<html>
<head>
  <title>Photobooth Payment</title>
  <script src="https://checkout.razorpay.com/v1/checkout.js"></script>
</head>
<body style="margin:0; padding:0; font-family:Arial, sans-serif; background:linear-gradient(135deg, #1a2a6c, #b21f1f, #fdbb2d); height:100vh; display:flex; justify-content:center; align-items:center;">

  <div style="background:white; padding:40px; border-radius:20px; box-shadow:0px 8px 20px rgba(0,0,0,0.2); text-align:center; max-width:400px; width:100%;">
    
    <h2 style="margin-bottom:20px; font-size:28px; color:#333;">Pay 10 to Start Photobooth</h2>
    <p style="margin-bottom:30px; font-size:16px; color:#555;">Unlock the configuration and start capturing amazing memories </p>
    
    <form action="/success" method="POST">
      <script
          src="https://checkout.razorpay.com/v1/checkout.js"
          data-key="{{ key }}"
          data-amount="1000"
          data-currency="INR"
          data-order_id="{{ order_id }}"
          data-buttontext="Pay Now"
          data-name="Photobooth"
          data-description="Unlock Photobooth Configuration"
          data-theme.color="#3399cc">
      </script>
    </form>
  </div>

</body>
</html>
"""


@app.route('/')
def index():
    # Create an order (?10 = 1000 paise)
    order = razorpay_client.order.create(dict(amount=1000, currency="INR", payment_capture=1))
    return render_template_string(html_template, key="rzp_test_R8Pjr1V054idbz", order_id=order['id'])

@app.route('/success', methods=['POST'])
def success():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    khichik_dir = os.path.join(base_dir, "..", "khichik")

    # Step 1: Run setup.sh (ensure cwd is khichik so `cd scripts/` inside works)
    setup_path = os.path.join(khichik_dir, "setup.sh")
    subprocess.run(["bash", setup_path], cwd=khichik_dir)

    # Step 2: Automatically run generated photobooth.sh
    photobooth_path = os.path.join(khichik_dir, "photobooth.sh")
    subprocess.Popen(["bash", photobooth_path], cwd=khichik_dir)

    return "? Payment Successful! Setup complete and photobooth.sh is running."

if __name__ == "__main__":
    # Open browser automatically
    app.run(host="127.0.0.1", port=5000)

