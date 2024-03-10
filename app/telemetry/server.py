from flask import Flask, send_file
import matplotlib.pyplot as plt

app = Flask(__name__)

@app.route('/')
def index():
    data = open('data/happiness.txt', 'r')

    # Data for the bar graph
    categories = ['Category 1', 'Category 2', 'Category 3', 'Category 4', 'Category 5']
    values = data.readlines()
    val = []

    for value in values:
        val.append(int(value.strip()))

    # Creating the bar graph
    plt.bar(categories, val, bottom=0)
    plt.xlabel('Categories')
    plt.ylabel('Values')
    plt.ylim(0)
    plt.title('Bar Graph')

    # Saving the plot as a temporary file
    temp_image = '/tmp/bar_graph.png'  # Temporary file location
    plt.savefig(temp_image)
    plt.close()

    # Serving the temporary image file
    return send_file(temp_image, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)