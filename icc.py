#! /usr/bin/python
# -*- coding:utf-8 -*-

# Idle Control Code = icc

from flask import Flask, render_template_string, redirect, request, send_from_directory
from RpiMotorLib import RpiMotorLib

#define GPIO pins
GPIO_pins = (14, 15, 18)
#Microstep Resolution MS1-MS3 -> GPIO Pin
direction = 20
#Direction Pin,
step = 21
#Step Pin
distance = 80
#Default move 1mm => 80 steps per mm

#Declare an named instance of class pass GPIO pins numbers
mymotortest = RpiMotorLib.A4988Nema(direction, step, GPIO_pins, "A4988")

app = Flask(__name__, static_url_path='')

#HTML Code
TPL = '''
<html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
        <!-- Bootstrap CSS -->
        <link rel="stylesheet" href="/css/bootstrap.min.css">
        <title>DSMtuned Idle Control</title>
    </head>
    <body>

<div class="container">
 <div class="row" style="padding:10">
  <form method="POST" action="moveMotor">
  <div class="btn-group-justified" role="group"style="padding:30" >
   <ul class="moveButtons">
   <li>
    <input type="radio" id="m50" value="50" name="amount" />
    <label for="m50">50</label>
   </li>
   <li>
    <input type="radio" id="m100" value="100" name="amount" checked="checked" />
    <label for="m100">100</label>
   </li>
   <li>
    <input type="radio" id="m150" name="amount" value="150" />
    <label for="m150">150</label>
   </li>
   </ul>
  </div>
</div>
<div class="row" style="padding:10">
<div class="btn-group-justified" role="group" style="padding:30" >
<input type="submit" name="action" class="btn btn-primary btn-lg" value="Up" />
<input type="submit" name="action" class="btn btn-primary btn-lg" value="Down" />
</div>
</div>
</form>
      </div>
</body>
</html>

'''

@app.route('/css/<path:path>')
def send_js(path):
    return send_from_directory('css', path)

@app.route("/")
def home():
    return render_template_string (TPL)

@app.route("/moveMotor", methods=["POST"])
def moveMotor():
    moveAmount = request.form
    #print(moveAmount['amount'], moveAmount['action'])
    if 'Up' in moveAmount['action']:
        print('GoingUp')
        mymotortest.motor_go(False, "Full", moveAmount['amount'], 0.01, False, .05)
    elif 'Down' in moveAmount['action']:
        print('GoingDown')
        mymotortest.motor_go(True, "Full", moveAmount['amount'], 0.01, False, .05)
    else:
        print("whoops, mama i'm confused")
    return redirect(request.referrer)

#Run the app on the local development server
if __name__ == "__main__":
       app.run()
