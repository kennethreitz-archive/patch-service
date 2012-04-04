Patch Service
=============

This is the web service that powers http://pat.ch.

Plans
~~~~~

- Force HTTPS
- Basic Authenticationm


URI Schema::

    /user
        username
        email
        bio
        website
        location
        date_joined
    /users/
    /users/:user/patches/
        name
        .. vanity_name?
        description
        distribution
        device
    /downloads/:id
        hash
        file_name
        file_size
    /devices/:slug
        slug
        vanity_name
        make
        model
    /category/:slug
        name
        vanity_name


Preset
Drum Sample
Synth Sample
