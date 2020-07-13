## Inspiration

We’ve all been part of the job process. It’s a long, gruesome process, where we have to create a resume, send it to the employer, and get a response many weeks later. We decided to create a simple, but revolutionary platform and standard to allow employers to receive information about potential employees.

## What it does

MasterProfile is a web application that has one input and two outcomes. First, the user inputs their entire profile and portfolio. They add items such as jobs, achievements, projects, skills, their bio, and more. For the first outcome, we auto-generate a completely free portfolio website for them that they can customize. They can share this website with anyone. 

The second outcome is based on our token system. Each user is assigned a token, and with that token, companies and employers can access the profile and portfolio of the user through our API. Our API has extensive documentation that employers can use. Our API is also built on our standard. We standardize the way users’ portfolio data is presented. No more hand-reading resumes with missing information and everything in different places. Our standardized API creates opportunities for portfolio automation and analysis. Along with the standardization comes new business models and opportunities. For example, if an employer wants to find which candidate is the best match, they can use a product which offers a rating to each candidate based on the job requirements, through machine learning. There can be entire products that are focused on assigning ratings to job candidates! This presents endless opportunities for companies and users alike.

## How we built it

This project required extensive backend and frontend development. The UI of our project was built using the Materialize CSS framework. Meanwhile, the backend of our project was built with Flask, the python-based web micro-framework. We are using Heroku to host our project, and we are also using a PostgreSQL database to handle user information and portfolios. 

Our UI design process was a multi-step process that was used to ensure the quality of the UI and UX. First, we wireframed our UI using Balsamiq. Then, we designed the rough UI with HTML, CSS, and JavaScript, using Materialize CSS. After that, we combined our frontend and backend to finish the UI. Finally, we quality controlled our UI and UX through testing. Our landing page was built with Bootstrap Studio, a WYSIWYG HTML editor.

Creating the backend was also a multi-step process. First, we created database models using SQLAlchemy, and created forms using Flask-WTforms. We eventually did the login and register pages, and then the portfolio management pages. Soon after, we wrote the code that auto-generated portfolio websites for every user. Finally, we wrote the API which allowed the companies and employers to get the data of users through the secure token. The API reference was generated using Stoplight.


## Challenges we ran into

We ran into multiple challenges when creating MasterProfile. The first challenge we ran into was allowing users to customize their portfolio websites. We had to use an unfamiliar Python library, Colour, to handle the color choosing aspect of our customization aspect. Another challenge was designing the landing page, known as the “How it works” page. That page was not designed using Materialize CSS, rather it was designed using Bootstrap Studio and a Bootstrap Studio template. We also had a particularly hard time of designing the way the user’s portfolio would be displaying, with Materialize carousels. For the backend, we had an issue developing the API, and returning the data in JSON format, so we developed our own method of returning the user’s information in JSON format.

## Accomplishments that we're proud of

We are proud that we built a fully-functioning web application with an extensive backend and stunning frontend. We are also proud of API, which allows employers to make data-driven decisions on who to employ. 

## What we learned

**Delegation & Teamwork**

We learned how to delegate tasks and assign tasks for different group members, so we could work simultaneously. For example, if Vishnu was working on the backend and the login and register pages, Lavan would be designing and building the frontend for those pages, and Pranav would be creating the associated database models. This delegation allowed us to work efficiently.

**Other**

We also learned how to wireframe our application with Balsamiq. Along with that, we learned how to create an API with a secure token system, as well as how to write API documentation using Stoplight.

## What's next for MasterProfile

First, we plan on defining an elaborate standard for the way the portfolio and profile information of a user is presented. We will expand this standard from what we have now with multiple additions. We will also work towards patenting the standard and marketing it to expand its usage.

Next, we plan on creating a machine learning integration for our product. We want to create a product that assigns ratings to potential candidates based on a list of requirements for a job. This will allow employers and companies to simplify their hiring process.