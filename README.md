WEVOLVER
========

[![Build Status](https://travis-ci.org/javaguirre/wevolver-server.png)](https://travis-ci.org/javaguirre/wevolver-server)

Introduction
------------

**Wevolver is an application for makers to share open hardware projects**  
Inspire others: present projects, connect, collaborate.  


#### Clearly present complex projects  
Developing hardware is a variable and unpredicatble process.
It makes documenting and presenting what you make a chore. Yet sharing your work
in progress opens up many possibilities to start a conversation, to get feedback, and to inspire people.  
Wevolver enables you to present your project clearly through a mind-map like structure.  


#### Connect with others through the projects you do  
It is not about how many connections you have, it is about meaningful connections.
Get in touch with others because of the projects you do, the skills you have,
and the things that interest you. Find people to work with or help out others!  
We call it project-based-networking.  


#### Keep overview in collaboration through a data-visualizing interface  
It is difficult to stay in control of the progress and activity of projects,
because hardware projects are multidisciplinary. Our interface gives you an instant
overview on your project, and gives access to in depth information about the state of your project.  


Visual. Intuitive. Fast.

Installation
------------

Wevolver is built with **Django** and **Tastypie**, you can install it through virtualenv using
the `setup_env.sh` script.

If you want to setup the testing environment you need to run the `build.sh` script defining `$WORKSPACE` as
the current directory of the project.

You can access the API through `/api/v1/`. You could start checking the [open projects][projects] or the [API documentation][api_documentation]

More detailed information coming soon.

Have fun!

[projects]: https://app.wevolver.net
[api_documentation]: http://localhost:8000/api/doc/
