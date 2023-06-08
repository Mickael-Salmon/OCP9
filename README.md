<div align="center">
  <a href="" target="_blank" rel="noreferrer">
    <img src="https://www.python.org/static/community_logos/python-logo-master-v3-TM.png">
  </a>
</div>


<h3 align="center">

Bienvenue ! Vous trouverez ici le Projet 9 du parcours<a href="https://openclassrooms.com/fr/paths/518-developpeur-dapplication-python" target="_blank" rel="noreferrer"> Développeur d'application - Python</a> 👋

</h3>

<h2 align="center">

Développez une application Web en utilisant Django 💻 !

</h2>

> Scénario
##

LITREVIEW a pour objectif de commercialiser un produit permettant à une communauté d'utilisateurs de consulter ou de solliciter une critique de livres à la demande.

</br>

<div align="center">
  <a href="" target="_blank" rel="noreferrer">
    <img src="https://user.oc-static.com/upload/2020/09/18/16004297044411_P7.png">
  </a>
</div>



</br>


💬 Objectif :
- mettre en place une application web pour notre MVP (minimum viable product, ou produit viable minimum).

</br>
💬 Cahier des charges

##
Summary
##

##
Signup and login functionality are a must in terms of what you need for this MVP. When a user logs into the system, their feed is the first page they will see. There they can see the tickets and reviews of all users they follow. They should also see their own tickets and reviews, as well as any reviews in response to their own tickets - even if they do not follow the reviewer. (The logic around combining querysets of different model types can be complicated. Check the appendix at the end of this specification for some guidance on how to do this.)
##
You can think of a ticket as a request for a review from a user. They post their ticket requesting a review for a book or literature article. Users who follow them can then submit their reviews in response to the ticket. Users should also be able to post reviews for books and articles that do not have a ticket yet.
##
Users will be able to follow other users and should also have the option to unfollow them. As this is just an MVP, keep this functionality fairly simple. You won’t need a search functionality or a Discover feed for new users. Keep it to a simple box where you enter the username of the user you wish to follow. You should also have a page that lists all the users the logged-in user follows with the option to unfollow.
##
You will also need another page from which users can review their own submissions. They should be able to see their posts and edit and delete them from this page.
##
Remember, this is an MVP, so try not to get too caught up on styling. Focus more on a clean and minimal UI. However, you  should ensure things like date formats, styling, etc. are consistent across the site. Follow the layout of the wireframes provided, but don’t be afraid to add some personal touches if you wish, remember, clean and minimal.
##
##
A user will need to:
##
    • Log in and sign up
    • the site should not be accessible to a non-logged-in user
    • View a feed containing the latest tickets and reviews from users that they follow ordered by time with the latest first.
    • Create new tickets requesting a review on a book/article.
    • Create reviews as a response to tickets.</br>
    • Create reviews not in response to a ticket.  As part of a one-step process, the user will create a ticket and then a review responding to their own ticket.
    • Be able to view, edit, and delete their own tickets and reviews
    • Follow other users by entering their username
    • View who they follow and unfollow whoever they want.
##
A developer will need to:</br>
##

    • Create a local environment using venv and run the site based on the detailed documentation laid out in the README.md.
##
The site will need to:</br>
##
    • Have a UI matching those of the wireframes.</br>
    • Have a clean and minimal UI.</br>
    • Use server-side rendering to display information from the database on the page dynamically.</br>
##
The codebase will need to:</br>
##
    • Use the Django framework.</br>
    • Use the Django template language for server-side rendering.</br>
    • Use SQLite as a local development DB (your db.sqlite3 file should be included in the repository).</br>
    • Have a database design that matches the database schema.</br>  Have syntax that meets PEP8 guidelines.</br>

##
LIVRABLES
##
Un document TXT contenant le lien vers le repository Github contenant un projet Django avec :</br>
- Un ensemble d'instructions détaillant la configuration de l’environnement et le fonctionnement de l'application.</br>
- L'application, qui répond aux exigences énoncées dans le cahier des charges, et présente une structure de base de données équivalente à celle du schéma de la base de données.</br>
- Une interface utilisateur correspondant à celle conçue dans les wireframes, s’affichant côté serveur à l'aide du langage de template Django.</br>

</br>

💬 Contraintes techniques:

</br>



> Livrables attendus 🔭
##



</br>

> Structure de dossiers du projet
##

```
├──
│   ├──
├──
│   ├──
└──
    ├──



```


<h2> Installation et démarrage du projet</h2>

<h3>Démarrer le server en local </h3>




<h3>Récupération du projet</h3>

$ git clone https://github.com/Mickael-Salmon/OCP9/

<h3>Lancer le programme </h3>


