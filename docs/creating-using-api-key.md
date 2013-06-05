HOWTO
=====

This tutorial will guide you on how to create an API Key for Wevolver and how to check it's working.

First we go to the /admin/ part of Wevolver and in the Oauth2 part we go to Clients.

Add Client and select a user from the list(when you click in the magnifying glass there is a list
of the current users), click in the name of the one you want to create a key for.

The application and redirect uri is not used already, but the client_id and secret will be our two
keys to request a token.

If our client_id is 5e93c2c71e4cb196c9e4 and our secret is 0aad4fe9cd12f9be51b1cfe77b451206d806564e we could test the request of the API like this.

    $ curl -d "client_id=5e93c2c71e4cb196c9e4&client_secret=0aad4fe9cd12f9be51b1cfe77b451206d806564e&grant_type=password&username=myemail@example.com&password=mypassword&scope=write" http://app.wevolver.net/oauth2/access_token

If everything is fine, the response will be:

    {"access_token": "a832106c17d00fd3b9094181c598820ef3ff76f4", "scope": "read write", "expires_in": 86399, "refresh_token": "bfdbd5510ae724a2dbd458e68274ab5c8590d3e4"}

There will be a new Access Token created in the Oauth2 Access Tokens table in the Django Admin. This means we could create it manually adding a new Access Token from the admin view, and not using the request explained before.

Now that we have the token we should be able to access our project with the next call:

    $ curl -v -H "Authorization: OAuth a832106c17d00fd3b9094181c598820ef3ff76f4" http://127.0.0.1:8000/api/v1/project/my_project_id/

Where my project id is the id of one of your projects, The response should response with a 200 and
the content of the project.

Source: http://ianalexandr.com/blog/building-a-true-oauth-20-api-with-django-and-tasty-pie.html
