import json


class Junction:
    def __init__(self, lane_id, no_of_lanes, green_min_time, green_max_time, pcu_dict):
        self.lane_id = lane_id
        self.green_min_time = green_min_time
        self.green_max_time = green_max_time
        self.pcu_dict = pcu_dict
        self.no_of_lanes = no_of_lanes
        self.api_count = [0] * self.no_of_lanes
        self.api_called = [False] * self.no_of_lanes
        self.priority_mask = [1.0] * self.no_of_lanes
        self.wait_time = [0] * self.no_of_lanes
        self.emergency_vehicles_count = [0] * self.no_of_lanes
        self.emergency_vehicles = [False] * self.no_of_lanes
        self.got_green_light = [False] * self.no_of_lanes

    def update_log(self, request):
        for i, req in enumerate(request):
            if i < len(self.api_called):
                self.api_called[i] = True
                self.api_count[i] += req

    def resolve_priority(self, current_vehicles={}):
        # current_vehicles={lane_no:{vehicle_type:count}}
        value = [0.0] * self.no_of_lanes
        for lane, values in current_vehicles.items():
            temp = 0.0
            for vehicle, count in values.items():
                if vehicle == "ambulance":
                    self.emergency_vehicles[lane] = True
                    value[lane] += 5 * count
                temp += count * self.pcu_dict.get(vehicle, {"pcu": 0})["pcu"]
            value[lane] += temp

        for i, api_freq in enumerate(self.api_count):
            if self.api_called[i]:
                value[i] += 0.5 * api_freq

        green_freq = sum(self.got_green_light)
        if green_freq == self.no_of_lanes:
            for i in range(self.no_of_lanes):
                self.got_green_light[i] = False
                self.priority_mask[i] = 1.0

        for i, mask in enumerate(self.priority_mask):
            value[i] *= mask

        max_lane = value.index(max(value))
        green_time = self.green_min_time if self.green_min_time > 0 else 0

        for i in range(self.no_of_lanes):
            if i != max_lane:
                self.priority_mask[i] += 0.3
            else:
                self.priority_mask[i] = max(0, self.priority_mask[i] - 0.2)
                self.emergency_vehicles[i] = False
                self.api_called[i] = False
                self.got_green_light[i] = True
                temp = sum(
                    count
                    * self.pcu_dict.get(vehicle, {"pcu": 0})["pcu"]
                    * self.pcu_dict.get(vehicle, {"time_per_unit": 0})["time_per_unit"]
                    for vehicle, count in current_vehicles[i].items()
                )
                green_time = max(green_time, min(self.green_max_time, temp))

        return max_lane, green_time


class TrafficSync:
    def __init__(self):
        self.lane_id_current = 0
        self.lane_id_list = []
        self.junctions = {}

    def get_junction_resolver(
        self,
        no_of_lanes=4,
        green_min_time=30,
        green_max_time=180,
        pcu_dict={
            "passenger_car": {"pcu": 1.0, "time_per_unit": 2.0},
            "two_wheeler": {"pcu": 0.5, "time_per_unit": 2.0},
            "bus": {"pcu": 3.5, "time_per_unit": 2.0},
            "auto_rickshaw": {"pcu": 0.75, "time_per_unit": 2.0},
            "bicycle": {"pcu": 0.2, "time_per_unit": 2.0},
            "ambulance": {"pcu": 2.0, "time_per_unit": 2.0},
            "truck": {"pcu": 3.5, "time_per_unit": 2.0},
            "van": {"pcu": 2.0, "time_per_unit": 2.0},
            "car": {"pcu": 1.0, "time_per_unit": 2.0},
        },
    ):
        lane_id = self.lane_id_current
        self.lane_id_current += 1
        self.lane_id_list.append(lane_id)
        self.junctions[lane_id] = Junction(
            lane_id, no_of_lanes, green_min_time, green_max_time, pcu_dict
        )
        return self.junctions[lane_id]

    def api_sync(self, requests={}):
        for junction_id, data in requests.items():
            if junction_id in self.junctions.keys():
                vehicles = data.get("vehicles", {})
                request = [
                    vehicles.get(vehicle, 0)
                    for vehicle in self.junctions[junction_id].pcu_dict.keys()
                ]
                self.junctions[junction_id].update_log(request)
        return None

    def synchronizer(self):
        # Under Development
        return None


TrafficManager = TrafficSync()

junction = TrafficManager.get_junction_resolver()

# Sample JSON input
json_data = [
    {
        "timestamp": 0.0,
        "road": 0,
        "vehicles": {
            "ambulance": 0,
            "bicycles": 1,
            "buses": 1,
            "trucks": 1,
            "vans": 0,
            "cars": 1,
            "trains": 1,
            "tractors": 0,
        },
    },
    {
        "timestamp": 0.0,
        "road": 1,
        "vehicles": {
            "ambulance": 0,
            "bicycles": 1,
            "buses": 1,
            "trucks": 1,
            "vans": 0,
            "cars": 1,
            "trains": 1,
            "tractors": 0,
        },
    },
    {
        "timestamp": 0.0,
        "road": 2,
        "vehicles": {
            "ambulance": 0,
            "bicycles": 1,
            "buses": 1,
            "trucks": 1,
            "vans": 0,
            "cars": 1,
            "trains": 1,
            "tractors": 0,
        },
    },
    {
        "timestamp": 0.0,
        "road": 3,
        "vehicles": {
            "ambulance": 0,
            "bicycles": 1,
            "buses": 1,
            "trucks": 1,
            "vans": 0,
            "cars": 1,
            "trains": 1,
            "tractors": 0,
        },
    },
]

# Parsing JSON input
current_vehicles = {}
for data in json_data:
    current_vehicles[data["road"]] = data["vehicles"]

TrafficManager.api_sync({0: current_vehicles})

max_lane, green_time = junction.resolve_priority(current_vehicles)
print("Max Lane:", max_lane)
print("Green Time:", green_time)
