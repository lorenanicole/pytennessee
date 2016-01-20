from flask import Flask, request
from cta_bustracker import CTABustracker
import json
from serializers import Prediction, MyEncoder

app = Flask(__name__)


@app.route('/')
def hello_world():
    return 'Hello World!'

@app.route('/compare_routes')
def compare_routes():
    threshold = 1320  # 0.25 mile in feet
    cta_client = CTABustracker()
    predictions = cta_client.get_stop_on_route_predictions(route_id=request.args.get('route'),
                                                           stp_id=request.args.get('current_stop_id'))

    closest = min(predictions, key=lambda x: abs(x.distance_to_stop - threshold))

    return json.dumps(closest, cls=MyEncoder)

if __name__ == '__main__':
    app.run()
