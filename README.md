# Scholar-Sync

Scholar-Sync is a web-based platform designed to facilitate the seamless distribution of research papers tailored to users' interests. It provides a user-friendly interface that allows researchers, academics, and knowledge enthusiasts to stay informed and connected to the latest advancements in their fields of interest. By streamlining the process of discovering and accessing research papers, Scholar-Sync simplifies the journey of exploring scholarly content and fosters a deeper engagement with the academic community.

## Key Features

- **User-Friendly Interface:** Scholar-Sync offers a user-friendly interface that allows users to create accounts and authenticate themselves. Upon logging in, users can specify their topic preferences by selecting the areas of research that align with their interests.

- **Personalized Recommendations:** Leveraging machine learning algorithms, Scholar-Sync analyzes the user's topic preferences and dynamically fetches relevant research papers from various trusted sources. These papers are then compiled and organized based on their relevance to the user's chosen topics.

- **Research Paper Collection:** Scholar-Sync utilizes web scraping techniques to gather research papers from reputable repositories and academic databases. The platform has scraped over 300,000 articles from the Springer website using Beautiful Soup. The keywords from the articles are stored in a dataframe, enabling efficient matching with user preferences.

- **NLP Processing:** Scholar-Sync employs Natural Language Processing (NLP) techniques to process the user's preferences or interested topics. By analyzing and extracting keywords from the user's input, the system matches the keywords with the stored dataframe to provide relevant research paper recommendations.

- **Profile Page and Preferences Management:** Users have access to a profile page where they can view their total interests and the total number of mails they have received to date. They can edit or delete their preferences at any time, allowing them to fine-tune their research interests.

- **Customizable Email Delivery:** Scholar-Sync sends recommendation emails to users based on their preferred frequency and time. Users can modify their email delivery settings on the profile page, selecting the desired frequency and time at which they wish to receive their emails.

- **Spam Prevention:** To prevent spamming, Scholar-Sync includes a model developed within the Django framework. This model ensures that already sent articles are not repeated and avoids overwhelming users' inboxes with duplicate content.

## Getting Started

To run Scholar-Sync locally, follow these steps:

1. Clone the project repository:
   ```
   git clone https://github.com/Hack-Shark/ScholarSync
   ```

2. Navigate to the project directory:
   ```
   cd ScholarSync
   ```

3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install `virtualenv`:
   ```
   pip install virtualenv
   ```

5. Create and activate a virtual environment:
   ```
   virtualenv env
   .\env\Scripts\activate
   ```

6. Navigate to the backend directory:
   ```
   cd backend
   ```

7. Apply database migrations:
   ```
   python manage.py makemigrations
   python manage.py migrate
   ```

8. Create a user account:
   ```
   python manage.py createsuperuser
   ```

9. Run the development server:
   ```
   python manage.py runserver
   ```

10. Copy the URL displayed in the terminal and paste it into your browser.

11. Access the admin panel:
    - Append `/admin` to the URL in the browser's search bar.
    - Login with the credentials of the user created in step 8.

12. Set user preferences:
    - Navigate to "Users Frequencies" in the admin panel.
    - Add frequencies according to your interests. The format is `Days Hours:Minutes:Seconds`.

13. Obtain research papers:
    - Visit the URL from step 10.
    - Provide your preferences in the command prompt.
    - Set the date to obtain articles published after a specified date.

14. Access the profile page:
    - Go to the profile page on the website.

15. Choose email delivery options:
    - Select the time at which you wish to receive your first email.
    - Choose the frequency at which you want to receive emails.
    - Save the details.

16. To obtain emails:
    ```
    send_emails_command
    ```

Feel free to make changes, extend the project, and add improvements as needed.

## Technologies Used

Scholar-Sync is built using the following technologies and tools:

- Django: A high-level Python web framework.
- Beautiful Soup: A Python library for web scraping and parsing HTML.
- Natural Language Processing (NLP): Techniques for analyzing and understanding human language.
- SMTP: Simple Mail Transfer Protocol for sending emails.

## Contributing

Contributions to Scholar-Sync are welcome! If you have any ideas, suggestions, or bug reports, please open an issue or submit a pull request on the project repository.

## License

Scholar-Sync is released under the [MIT License](https://opensource.org/licenses/MIT). Feel free to use, modify, and distribute the code.
