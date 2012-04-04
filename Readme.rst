Patch Service
=============

This is the web service that powers http://pat.ch.

Plans
~~~~~

- Force HTTPS
- Basic Authentication


URI Schema::

    /user
        username
        email
        bio
        website
        location
        date_joined
    /users/
    /users/:user/packs/
        name
        .. vanity_name?
        description
        patches
    /users/:user/patches/
        name
        .. vanity_name?
        description
        distribution
        device
    /distributions/:id
        hash
        file_name
    /devices/:slug
        slug
        vanity_name
        make
        model
        approved

