# Distinctiveness and Complexity

My web application, "Quantifique", is a unique and complex platform designed to provide personalized investment recommendations to users based on validated trading strategies.

My project includes various django models, utilizes JS and CSS, and is mobile responsive.

The user can create an account, log in and log out, and have a very clear interface that shows what are their recommendations, with entry price, stop loss and target.

It also includes a strategy and date filter, so that the user can more closely see what matters to them.

It goes beyond the scope of previous projects in CS50WEB by having:
- an infinite scroll feature that works with the unique datetime and strategy filters (CS50WEB teaches pagination without infinite scrolling);
- having "PT-BR" language location that impacts especially number separators and datetime formatting (other CS50WEB projects uses "US" location);
- implementing custom templatetags (other CS50WEB projects only uses default templatetags);
- implementing custom form validators (other CS50WEB projects only uses default validators);
- uses custom cookies (other CS50WEB projects don't require the use of custom cookies);
- being generally optimized to run with the lowest number of server requests possible.

# How to Run

Install project dependencies: `pip3 install -r requirements.txt`

Migrate the DB: `python3 manage.py migrate`

On your terminal, run `python3 manage.py runserver`

Create an account, then login

Go to the route `/new_call`

Go back to the route `/` -> You should see one call now

You can filter by strategy or date.

# Investments Recomendations WebApp

## folder `main`:

### file `forms.py`:

Creates an user registration form based on the default django form. Includes username, e-mail, first name, last name, cpf and password

cpf is an abbreviation to "Cadastro de Pessoa Fisica" in Brazil. It's the person's social security number.

### file `validators.py`:

Verifies if the inputted CPF is valid according to brazilian laws.

### file `models.py`:

Includes all models used in the project.

The `User` model inherits from `AbstractUser` plus an added cpf field

The `Strategy` model defines an investment strategy.

The `StrategyStat` model defines the stats of a trading strategy.

The `StrategyParam` model defines the currency for a given strategy.

The `Symbol` model defines a symbol used to make trades/investments.

The `StrategyCall` model is responsible to store and control all the recommendations given.

### file `urls.py`:

Defines all urls used by the app.

### file `views.py`:

Where the backend happens

When an web request is made, some view is processed.

`home`: renders index.html passing all strategies.

`calls`: is an API that returns all recommendations for a given page; also handles the filters using cookies.

`calls_api`: creates and updates investment recommendations.

`login_view`: renders login.html that prompts the user to log in.

`logout_view`: logs out the user

`register`: renders register.html that gives and user registration form.

## folder `main/static/main`:

#### The static folder is used to serve static files such as CSS, JavaScript, images, and other assets that are required by the web application. It provides a centralized location to store these files and makes them accessible to the web server during the development and deployment of the project.

### file `index.js`:

- DOMContentLoaded Event Listener: 
The listener ensures that the JavaScript code executes only after the HTML content has fully loaded.

- Populate Content Body:
The `populateBody()` function is called to populate the content body with call cards. This function retrieves data from the server endpoint, retrieves call information, and dynamically creates call cards to display on the web page.

- Datetime Filter: 
The code initializes a date picker element (`datepicker`) and retrieves filter start and end dates from cookies (`filterStartDate` and `filterEndDate`). If the start and end dates are available, they are parsed and assigned to `filterStartDate` and `filterEndDate` variables as `Date` objects.
A date picker is created using the `easepick` library with various configuration options. The initial date range for the date picker is set using `filterStartDate` and `filterEndDate`. Event listeners are attached to the date picker to handle date selection and clear events.
When a date range is selected or cleared, the corresponding start and end dates are stored in cookies (`filterStartDate` and `filterEndDate`). After updating the date filter, the `clearBody()` and `populateBody()` functions are called to update the displayed call cards based on the new date range.

- Strategy Filter Handler: 
The code initializes a strategy filter element (`#strat-filter`) and retrieves the selected strategies from cookies (`filterStrategies`). The selected strategies are stored as an array in the `filteredStrats` variable. Event listeners are attached to the strategy filter to handle changes in the selected options.
When a strategy option is clicked, the selected strategies are updated, and the `filterStrategies` cookie is updated accordingly. After updating the strategy filter, the `clearBody()` and `populateBody()` functions are called to update the displayed call cards based on the new filters.

- clearBody() Function: 
This function removes all existing call cards from the DOM by selecting elements with the class `.strategy-card` and removing them one by one. It is used to clear the content body before populating it with new call cards.

- populateBody() Function: 
This function populates the content body with call cards. It starts by fetching call data from a server endpoint (presumably `/calls/1`) using the `fetch()` function. The response is expected to be in JSON format, which is then processed in the following steps.
The call data is iterated through, and for each call, the `createCallCard()` function is called to generate a call card and append it to the content body.
After the initial call cards are loaded, the function sets up a scroll event listener (`document.onscroll`) to load more call cards when the user reaches the bottom of the page. The scroll listener checks if there is a next page (`has_next`) and if the user has scrolled to the bottom of the page. If both conditions are met, a new fetch request is made to load the next page of call cards.

### file `styles.css`:

#### This CSS file defines the styles for a demo interface. It includes various selectors and properties to customize the appearance of the elements.

- The file starts with an import statement to include the Montserrat font from Google Fonts. Then, it sets the `font-family` for the entire body to `'Montserrat', sans-serif`, and sets the background color to `#fafafa`.

- The next section defines styles for anchor tags and their hover/focus states. It sets the color to `inherit`, removes the text decoration, and adds a transition effect.

- The `.navbar` class styles the navigation bar, including padding, background color, border, border-radius, margin, and box-shadow properties.

- The `.navbar-btn` class styles the buttons within the navigation bar, removing `box-shadow` and `outline`, and setting the border to `none`.

- The `.line` class defines a horizontal dashed line with a width of 100%, a height of 1px, and a color of `#ddd`. It is used to separate sections.

- The `span` selector sets the `display` property to `inline-block`.

- The `.wrapper` class defines a flex container with the `align-items` property set to `stretch`.

- The following section focuses on the sidebar styles. The `#sidebar` ID sets the minimum and maximum widths, background color, and text color. It also includes transition effects for resizing.

- The `#sidebar .sidebar-header h3` styles the header of the sidebar, setting the margin to 0.

- When the sidebar is in the active state (narrower width), the styles change. The width is reduced, the text alignment becomes center, and certain elements such as the header and sidebar text are hidden.

- The `.CTAs` class within the sidebar is hidden in the active state.

- The `#sidebar ul li a` selector styles the links within the sidebar, setting text alignment to left.

- In the active state, the padding, text alignment, and font size of the links are modified.

- The `.dropdown-toggle::after` selector styles the arrow icon that appears next to dropdown menus.

- The `ul` and `li` selectors define styles for unordered lists and list items within the sidebar.

- The styles for the content area (`#content`) include width, padding, minimum height, and transition effects.

- The `.content-header` and `.content-body` classes define styles for the header and body of the content area.

- The `#row-filter` and `.col-filter` selectors style specific elements related to filtering options.

- The `.dropdown.bootstrap-select.show-tick` class styles the dropdown select elements with a tick icon.

- The `#datepicker` selector styles a date picker element.

- The `#row-main` and `.strategy-card` selectors style specific elements within the main content area.

- The styles for the cards and their headers, bodies, and descriptions are defined.

- The media queries section includes styles for responsive design, adjusting the layout and sizing of elements for screens with a maximum width of 768px.

## folder `main/templates/main`:

### file `layout.html`:

1. `{% load static %}`: This is a Django template tag used to load the static files from the `static` directory.

2. `<link rel="stylesheet" href="{% static 'main/styles.css' %}">`: This line includes a CSS file named `styles.css` from the `main` directory in the static files.

3. `<script src="https://cdn.jsdelivr.net/npm/@easepick/bundle@1.2.0/dist/index.umd.min.js"></script>`: This line includes the easepick JS file to create the strategies filter.

4. `{% block script %} {% endblock %}`: This is a Django template block tag that defines a block named `script`. Other templates that inherit from this template can override this block and insert their own JavaScript code.

5. The code defines a sidebar navigation menu with two list items (`Home` and `Sair`). Each list item has an associated URL and an icon. The URLs are either empty or generated using Django's `{% url %}` template tag.

6. The content area of the page is divided into a content header and content body. The content header displays the current date using Django's `{% now %}` template tag.

7. The code includes several external JavaScript libraries, including jQuery, Popper.js, Bootstrap JS, and Bootstrap Multiselect. These libraries enhance the functionality and appearance of the web page.

8. The final JavaScript code is responsible for toggling the sidebar when the "sidebarCollapse" element is clicked. It adds or removes the "active" class from the sidebar element, which is defined in the CSS file.

### file `index.html`:

1. This Django template extends the "main/layout.html" template and loads static files using the `{% load static %}` tag.

2. The template defines a "body" block where the main content will be placed. Inside this block, there is a container `<div>` with the ID "container-main".

3. Within the container, there is a row with the ID "row-filter". Inside this row, there is a column with the class "col-filter". Within this column, there is a `<select>` element with the ID "strat-filter" and an `<input>` element with the ID "datepicker".

4. The `<select>` element represents a dropdown for filtering strategies. It allows multiple selections and displays the count of selected items. The options are generated dynamically using a loop over the "strategies" variable.

5. The `<input>` element is used for filtering by date and has a placeholder text.

6. After the "row-filter" section, there is another row with the ID "row-main". This row is likely used for displaying the main content of the page.

7. The template includes a "script" block where an external JavaScript file, "main/index.js", is included using the `{% static %}` tag.


### files `login.html` and `register.html`:

Just templates to their respective functions.

## folder `main/templatetags`:
### file `main_extras.py`:
Used to create an `addstr` function that can be used in the HTML template and concatenates two strings.
