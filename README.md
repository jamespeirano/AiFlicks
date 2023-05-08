# AI Flicks
This is a web application that utilizes image generator APIs to generate an image based on user's text input, and displays it on a print-on-demand product such as a t-shirt.

The application works by taking user's input and sending it to the API, which generates an image based on the input. The generated image is then displayed to allow the user to see what the image would look like on a t-shirt.

## Getting Started
To get started with this application, you will need to do the following:

- Clone this repository to your local machine.
- Install the necessary dependencies.

## Usage
Once the application is running, you can access it by navigating to http://localhost:3000 in your web browser. You will see a form where you can enter your text input. Once you have entered your input, click the "Generate Image" button.

The application will then send your input to the OpenAI Dalle API, which will generate an image based on your input. The generated image will be displayed on the right side of the web page, next to a blank image of a t-shirt.

To see what the image would look like on a t-shirt, select a t-shirt size and color from the dropdown menus, and click the "Preview on T-Shirt" button. The application will then send the generated image and t-shirt information to the Printful API, which will generate a mockup of the t-shirt with the generated image on it.

You can then see the mockup by scrolling down to the "T-Shirt Preview" section on the web page.

Contributing
If you would like to contribute to this project, feel free to submit a pull request. Please ensure that your changes adhere to the coding style and guidelines used in this project.

License
This project is licensed under the MIT License. See the LICENSE file for details.
