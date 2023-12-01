from flask import Flask, jsonify, request

app = Flask(__name__)

# Priority Queue to store animal reports
class PriorityQueue:
    def __init__(self):
        self.queue = []

    def enqueue(self, animal, injury, location):
        priority = 0 if injury == 'Mild' else 1 if injury == 'Medium' else 2
        index = 0
        for item in self.queue:
            if item[0] < priority:
                break
            index += 1
        self.queue.insert(index, (priority, {'animal': animal, 'injury': injury, 'location': location}))

    def dequeue(self):
        if self.is_empty():
            return None
        return self.queue.pop(0)[1]

    def is_empty(self):
        return len(self.queue) == 0

    def get_all_reports(self):
        return [item[1] for item in self.queue]

# Sample priority queue with initial records
animal_priority_queue = PriorityQueue()
animal_priority_queue.enqueue('Dog', 'Mild', 'Park A')

@app.route('/animal_reports', methods=['GET'])
def get_animal_reports():
    # Retrieve all animal reports from the priority queue without clearing it
    reports = animal_priority_queue.get_all_reports()

    # Return the animal reports as JSON
    return jsonify({'animal_reports': reports})

@app.route('/clear', methods=['GET'])
def clear_queue():
    animal_priority_queue.queue = []
    return jsonify({'message': 'Queue cleared successfully'})

@app.route('/add', methods=['GET', 'POST'])
def add_animal_report():
    # Extract animal details from the query parameters or JSON
    animal = request.args.get('animal') or request.json.get('animal')
    injury = request.args.get('injury') or request.json.get('injury')
    location = request.args.get('location') or request.json.get('location')

    # Add the new animal report to the priority queue
    animal_priority_queue.enqueue(animal, injury, location)

    # Return a success message
    return jsonify({'message': 'Animal report added successfully'})

if __name__ == '__main__':
    # Run the application on port 5000
    app.run(port=5000, debug=True)
