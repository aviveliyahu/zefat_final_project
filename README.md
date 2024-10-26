Our final project combines LLM powers with our own unique data in each category (gathered using RAG from pinecone DB we created). the main poropuse is to be a chatbot that helps a therapy interns with their question using the Socratic method.<br>
In order to show our capabilities, we also added option to use different LLMs (such as openai and claude) and more type of users such as amateur cook.<br>
Each type of user group has its own designated prompt, database and information in order to provide a rich and infomative answer.<br>
There are also two types of users - regular and admin. both have the same chat screen but admins also has admin panel to create new users as admins or regular users - the group is set automatically (corresponds to the admin's type of group)<br>
User can also save the chat (locally) in order to re-read the conversation he had.
<br>
<h4>Here are some pictures of the project running</h4>
<h5>Login page picture</h5>
![login](https://github.com/user-attachments/assets/d3d197e2-3a80-49d5-90c7-df3178a55f34)

<h5>Main page (with admin panel)</h5>
![main](https://github.com/user-attachments/assets/e9f412ee-6141-45ab-b32c-35a984bcd37c)

In order to run the project, use the following steps:
1. clone project
2. create a virtual environment : python -m venv venv
3. enter the virtual environment : venv\scripts\activate
4. upgrade pip: python -m pip install --upgrade pip
5. install requirments.txt file : pip install -r requirements.txt
6. place .env file in main project folder, the file need to have the following details:
   * OPENAI_KEY
   * CLAUDE_KEY
   * PINECONE_KEY
   * MONGODB_USER
   * MONGODB_PASS
   * NAMESPACE
   * CASES_INDEX
   * ARTICLES_INDEX
   * RECIPES_INDEX
7. run app.py
8. enjoy!
