Bulawayo City - Project Management Dashboard
Project Overview

This is a project management dashboard developed for the Bulawayo City Council. The application allows users to log in with roles assigned to them (such as admin or regular user), providing access to a dashboard that displays important project metrics and data. Administrators have additional functionality to manage data via CRUD operations.

Key Features:

    Mobile Responsive: The dashboard is built with responsiveness in mind, ensuring smooth access and interaction from desktops, tablets, and smartphones.
    User Authentication: Role-based login for users and administrators.
    Admin Dashboard: Allows CRUD operations for project data.
    User Dashboard: Displays dynamic charts and tables for project management.
    Data Visualization: Graphs and tables to monitor project performance and progress.
    API Access: The dashboard can generate secure APIs to allow authorized data analysts to access and analyze the company's projects data for in-depth investigations.

Architecture & Technologies

This project is built using the following technologies:

    Front-end:
        HTML, CSS, JavaScript
        Bootstrap (for responsive UI design)
        Plotly (for interactive charts)
        Datatables (for interactive and dynamic tables)

    Back-end:
        Python Flask (for building the backend API and managing routes)
        MySQL Database (for storing project data)
        Authentication (role-based access control)

Development Report
Successes

    Implemented login functionality with user role authentication using Flask.
    Developed dynamic dashboards using Plotly for charts and Datatables for tables.
    Integrated CRUD operations into the admin dashboard for effective data manipulation.

Challenges

    Limited time to optimize code for performance.
    Difficulty selecting the right graphing tool, ultimately choosing Plotly.
    Managing integration between various technologies in the Flask framework.

Areas for Improvement

    Improve the speed of page loading, particularly on chart-heavy pages.
    Add more features to enhance user experience, such as advanced analytics.
    Improve the layout and user interface of the dashboard for better usability.

Lessons Learned

    Optimizing for performance while maintaining functionality is crucial for user experience.
    Flask is a flexible framework but requires careful planning for large-scale projects.
    Selecting the right tools at the start can save time later in development.

Next Steps

    Performance Optimization: Focus on optimizing page load times, especially with data-heavy pages.
    Feature Expansion: Add additional features such as project file management and task assignment.
    Layout Enhancements: Refine the user interface for a more intuitive and fluid experience.

Conclusion

Developing the Nando Construction Project Management Dashboard was an exciting and rewarding experience. I had the opportunity to integrate a variety of technologies and create a functional product that could be adapted for use by real companies. Looking forward, I am excited to continue refining the project, improving its performance, and adding new features.

Installation & Setup
Requirements

    Python 3.x
    Flask
    MySQL

Steps

    Clone the repository:

    bash

    git clone https://github.com/dylanmlilo/alx-project-management-dashboard.git

Install dependencies:

    bash

    pip install -r requirements.txt

Set up the MySQL database and update the Flask configuration for database credentials.

Run the project on your local server:

    bash

    flask run
