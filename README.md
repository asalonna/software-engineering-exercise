# software-engineering-exercise

How to run:

1. Activate virtual environment.
2. Install dependancies using pdm sync
3. Create an empty database using postgresql. Use the following command, inserting the name of the database in the appropriate field:
   CREATE DATABASE name
   ENCODING = 'UTF8'
   CONNECTION LIMIT = -1;
5. Create a .env file and add the following line: "DATABASE_URL = 'postgresql://postgres:[password]@localhost/[name]'"
   changing the sections in the []. This should use the password for the default user postgres on your computer, and the name of the database.
   If the password were 'password', and the name 'db', the result would be the following:
   DATABASE_URL = 'postgresql://postgres:password@localhost/db
7. Run "pdm run alembic stamp head" and "pdm run alembic revision --autogenerate -m "New Migration"" to populate the created database.
8. Run "uvicorn main:app --reload" to run the API server
9. Open the index.html using the live server vscode extension or similar


Features that would be needed in the future:

1. Being able to determine which features of the message have been coded upon hovering over them with the mouse would be a beneficial
   feature. This would enable the user to more easily and quickly determine the codes for each section of a message in the event that
   the tabular data for that message is too long to easily browse.
2. If the table of data on a page becomes too long, it should be truncated with multiple pages.
3. An account system would be a useful feature to ensure better moderation of message coding. An account system would enable a moderation queue to be
   added, where other users can check the codes submittied by their colleagues to prevent mistakes or poor labelling of the data.
   To compensate for this, in my design I allowed a 'Delete' option to allow the removal of a code in the event of something like a mistake.
   A risk with this is that anyone could delete any code, so there would need to be safeguards to prevent abuse of this feature.

   
Design Justification:

In my design, codes can be added to a portion of a message by selecting a phrase and using the dropdown to add a code to that phrase.
I considered other methods, such as colour coding the different parts of a message but decided against this for multiple reasons.
For instance, it would be quite difficult to create an easy to understand way of displaying a phrase that had been labelled with
multiple codes. 
This could be facilitated by enabling codes to be displayed by hovering over a highlighted section, however this
would be complex to implement for separate substrings containing some overlapping codes but having their own separate codes too.
Therefore, I decided to display the code for a given section of a message in a table where it is easily visible which code belongs to each
section. 
I did consider the option of colour coding the code names in the column to make them more immediately distinguishable, but 
if more codes were added to the system then this would not be scaleable as there might not be enough distinct colours to make sure codes are distinguishable.

In the 'Messages' page, a table of messages is displayed with brief information such as their IDs, text, and codes assigned. 
The table also lets users click on the ID of a message to view a more detailed breakdown of information, such as a breakdown of 
codes assigned to that message, as well as an ID of a message linked to this one (called Sibling ID). 
This was done in order to allow a way
to pair messages, for instance if they belonged to the same conversation.

The data is stored in the database in such a way so that the substrings and their corresponding codes are easily extractable in order to be used to
train a machine learning algorithm.

