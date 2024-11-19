# Discogs Recruiting Takehome Assignment: Token Blacklisting

Thanks for applying at Discogs!

We want to assess your technical ability, but we also think coding under pressure in an interview is a terrible way to do that. As a compromise, here's a takehome exercise that's a simplified version of work you'd be doing at Discogs if you were hired.

Our expectations are that you deliver functional software including readable, concise and maintainable code with some production considerations.

If we've made an error so grievous that you don't think you can finish the assignment, or you have any other questions after reviewing this document, feel free to email your contact at Discogs and let us know.

## Description of the Problem

At Discogs, we make use of [JSON Web Tokens (JWTs)](https://jwt.io/introduction) for securely transmitting information between parties.

Because JWTs are stateless, by design they cannot be revoked once issued and remain valid until they expire.

Your assignment is to create a simple token [blacklisting](https://en.wikipedia.org/wiki/Blacklist_(computing)) management service that can be used to blacklist a given JWT provided by the client so that it can no longer be used by the API.

## Setup

In this directory, we've included everything you should need to run a simple Flask-based API using Docker Compose.

In case you're not too familiar with [Flask](https://flask.palletsprojects.com/en/3.0.x/), [Python](https://www.python.org/), or [Docker](https://www.docker.com/), we've included a sample `/info` API endpoint to illustrate how routing and responses work.

Assuming you have a working Docker installation locally, you should be able to run `docker-compose up` to start the app. Once the app is running, it should be accessible on port `35000` of your docker machine's IP address.

If you'd like to use a different runtime environment than `Docker` and `Python`, that's totally fine.
Please include instructions on how to run your application, in that case.

For decoding JWTs, we've included the [PyJWT](https://pyjwt.readthedocs.io/en/stable/) library, although you may use another library if you prefer.

To keep things simple, we're using the HS256 signing algorithm and `discogs` as the secret key for creating and verifying JWT signatures.

We've also included a [Postman](https://www.postman.com) collection that can be used to test your API implementation.

Feel free to provide any feedback about the problem or this prompt, e.g. as comments in your code.

## Requirements

Please add the following endpoints to this API:

- A `POST /blacklist` endpoint that can be used to add a given JWT to the blacklist:
    - On success, subsequent calls to the `/info` API endpoint with the same JWT should return an error response indicating the token is blacklisted.
    - The return value should be a `JSON` object restating the request parameters and if the blacklisting operation was successful.
- A `DELETE /blacklist` endpoint that can be used to remove a given JWT from the blacklist:
    - On success, subsequent calls to the `/info` API endpoint with the same JWT should return a successful response since the token is no longer blacklisted.
    - The return value should be a `JSON` object restating the request parameters and if the blacklist removal was successful.

Please update the following endpoint in this API:
- The `GET /info` endpoint should:
    - Check the token blacklist and return an error response if the provided JWT by the client is blacklisted.
    - Return a value that is a `JSON` object restating the request parameters and the decoded token contents on success.

For all API endpoints:
- Validate that the provided JWT by the client was issued by `https://www.discogs.com/` and has not expired.
- Require Authorization with the Bearer authentication scheme from the client.

## Tips
- Keep it simple!

## Submission

To submit your solution:
- Create a private Github Repository that contains your code.
- [Invite](https://docs.github.com/en/account-and-profile/setting-up-and-managing-your-personal-account-on-github/managing-access-to-your-personal-repositories/inviting-collaborators-to-a-personal-repository) **anni3f**, **ebenStickney**, **dlowder**, **myusic**, **ironfroggy**, and **gbrough** as contributors.
- Let us know you have finished the solution by emailing your contact at Discogs.

See you soon, and thank you!

Discogs

