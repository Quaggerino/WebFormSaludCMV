# MonitoreoSaludCMV

This Flask application is designed to collect health-related survey data from patients and store it in a MongoDB collection. The survey aims to gather feedback regarding health services in Valparaíso. Here is a brief explanation of each segment:

1. **Environment Variables**: The app begins by loading `.env.development` file where sensitive information is stored like the `SECRET_KEY` for Flask and the MongoDB connection URI.

2. **Flask Configuration**: The application is configured with a secret key fetched from the environment variables for session management.

3. **MongoDB Setup**: It establishes a connection to MongoDB using the `MONGODB_URI`. It defines which database and collection to use (`cmvalparaisoDas` database and `opinionSaludValparaiso` collection).

4. **Rate Limiting**: To prevent abuse, a rate limiter is applied using `RATE_LIMITER_URI`, restricting users to 60 requests per 30 minutes.

5. **Content Security Policy**: A CSP header is added to all responses for additional security.

6. **Home Route**: The root route (`/`) handles both GET and POST requests for the survey form.
   - On POST, it validates and extracts data from the form fields, such as age, gender, health center, visit frequency, satisfaction level, recommendation level, and reasons for the given ratings.
   - The data is inserted into the MongoDB collection with the current date and a static target value.
   - After successful submission, the user is redirected to a thank-you page.

7. **Error Handling**: Custom error handlers are set up for 404 (Not Found), 500 (Internal Server Error), and 429 (Rate Limit Exceeded).

8. **Running the App**: At the end, the application is set to run in debug mode.

### HTML Template Overview:

The HTML template renders a survey form with various input fields:

1. **Basic Setup**: It sets the document type, language, character set, and viewport settings. It includes a title and a link to the CSS stylesheet.

2. **Survey Form**:
   - It includes fields for age, gender, affiliated health center (CESFAM), frequency of visits, satisfaction level, and likelihood of recommending the center.
   - Satisfaction and recommendation levels use a visual scale with interactive elements (though the actual JavaScript functions `highlightNumber()` are not provided here).
   - Users can provide a reason for their ratings in a text area.
   - A character count for the text area is also displayed.

3. **Submission**: The form is submitted via POST to the home route for processing.

4. **FAQ Link**: An accessible link to a FAQ page is provided, featuring a question mark icon and a decorative arrow.

5. **Scripts**: The template links to an external JavaScript file, presumably for form interactions and validation.

### Comments on the Implementation:

1. **Accessibility**: The use of `aria-label` in the FAQ link improves accessibility for screen reader users.
   
2. **Validation**: While the Flask app attempts to validate data on the server-side, there is no client-side validation visible in the HTML provided, except for some constraints on the input fields like age range.

3. **Security**: The CSP is a good practice, but the use of `'unsafe-inline'` for script and style sources undermines its effectiveness. This should be addressed if possible.

4. **Styling**: The form uses a separate CSS file, which isn't provided but is referenced in the HTML.

5. **Error Handling**: The server-side application has error handlers in place to provide feedback to the user in case of HTTP errors.

6. **Rate Limiter Feedback**: In case of rate limiting, a custom message is displayed, but it may benefit from providing the user information on when they can make a request again.

7. **Static Content**: Static content like CSS and images is served through dedicated routes, which use Flask's `url_for` function to generate URLs.
