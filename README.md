# Scholar-Sync
#### <i>  Web-based platform designed to facilitate the seamless distribution of research papers tailored to users' interests. </i>

<ul>
  <li>
    The website provides a user-friendly interface that allows users to create accounts and authenticate themselves. Upon logging in, users can specify their topic   preferences, selecting the areas of research that align with their interests. This personalized preference information serves as the foundation for ScholarSync's recommendation engine.
  </li>
  <li>
    Utilizing machine learning algorithms, ScholarSync analyzes the user's topic preferences and dynamically fetches relevant research papers from various sources.   The platform employs web scraping techniques to gather papers from trusted repositories and academic databases. These research papers are then compiled and organized based on their relevance to the user's chosen topics.
  </li>
  <li>
    With ScholarSync, researchers, academics, and knowledge enthusiasts can stay informed and connected to the latest advancements in their fields of interest. By streamlining the process of discovering and accessing research papers, ScholarSync simplifies the journey of exploring scholarly content and fosters a deeper engagement with the academic community.
  </li>
  <li> Run locally </li>
  <li> Clone the project <li>
  <pre> https://github.com/Hack-Shark/ScholarSync </pre>
  <li> Go to the project directory </li>
  <pre> cd ScholarSync </pre>
  <li> Install Dependencies</li>
  <pre> pip install -r requirements.txt </pre>
  <li>Install virtualenv </li>
  <pre> pip install virtualenv </pre>
  <pre> virtualenv env </pre>
  <li> Activate env </li>
  <pre> .\env\Scripts\activate  </pre>
  <li> Go to backend directory </li>
  <pre> cd backend </pre>
  <li> Make migrations </li>
  <pre> python manage.py makemigrations </pre>
  <pre> python manage.py migrate </pre>
  <li> Create a user account </li>
  <pre> python manage.py createsuperuser </pre>
  <li> To run server </li>
  <pre> python manage.py runserver </pre>
  <li> Paste the url present on the screen in the browser </li>
  <li> Go to admin panel </li>
  <li> add /admin to the url in search bar </li>
  <li> Login with the credentials of the user created before</li>
  <li> Go to users frequencies and add some frequencies according to your interest </li>
  <li> The format is Days Hours:Minutes:Seconds </li>
  <li> Now paste the 1st url in the browser </li>
  <li> Give the preferences in the command prompt</li>
  <li> Set the date to obtain articles published after specified date </li>
  <li> Go to profile page </li>
  <li> Choose the time at which you wish to recieve your 1st mail </li>
  <li> Choose the frequency at which you have to recieve mails </li>
  <li> Save the details </li>
  <li> To obtain mails </li>
  <pre> send_emails_command </pre>
</ul>


