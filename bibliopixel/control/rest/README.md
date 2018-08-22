The REST control opens four Endpoints that allow you to get and set Fields in
BiblioPixel Objects by Address.

* The **Basic Get Endpoint** and **Basic Set Endpoint** are simplified for
casual users.

* The **Single Endpoint** provides a REST API to `GET` and `PUT` a BiblioPixel
Object Field.

* The **Multi Endpoint** provides a REST-like API to `GET` and `PUT` multiple
BiblioPixel Object Fields.

---

The Basic Get Endpoint looks like /get/<address>.  It returns JSON which
contains exactly one of two fields:

* `"value"`, representing the BiblioPixel Object or Field at that Address
* `"error"`, representing an error that occurred

The Basic Set Endpoint is /set/<address>/<value> - it sets a Field in a
BiblioPixel Object.  <value> is a URL-quoted string containing YAML or JSON.

For casual use, the two Basic endpoints are easiest to use, because they
just respond to `GET` methods - "pasting a URL into a browser".

*Examples of Basic endpoints*

In the example projects/26-simple-rest.yml:

1. `http://localhost:8787/get/animation.levels` returns a JSON list of the
levels for each animation, `[0, 0, 0]` at the start.

2. `http://localhost:8787/set/animation.levels[2]/1` sets the level of the
third animation to be `1`.

---

The Single Endpoint, /single/<address>, provides a strict
`GET`/`PUT` REST API for one BiblioPixel Object or Field at a time.

With the `GET` method, this endpoint returns the same JSON as the Basic Get
Endpoint does.

With the `PUT` method, it sets the value of a BiblioPixel Object Field
from the form data with key `"value"` and returns an empty object, or it returns
a JSON object with just a single field `"error"`.

*Examples of the Single endpoint*

Again looking at projects/26-simple-rest.yml:

1. `GET`ting `http://localhost:8787/single/animation.levels` again returns
`[0, 0, 0]` at the start.

2. `PUT`ting `http://localhost:8787/single/animation.levels[2]` with
form data `value=1` sets the level of the third animation to be `1`.

---

The Multi Endpoint, /multi or /multi/<address>, provides a `GET`/`PUT`
REST-like API for multiple BiblioPixel Objects or Fields at one time.

The `GET` method uses the keys in the HTTP request dictionary as
BiblioPixel Object or Field Addresses, and returns a dictionary
mapping the Addresses to their JSON values.

The `GET` method uses the keys and values in the HTTP request dictionary as
to set BiblioPixel Object Fields using the key as the Address.

If an `<address>` field is provided, then this is prepended onto each key.

*Examples of the Multi endpoint*

From projects/26-simple-rest.yml again:

1. `GET`ting `http://localhost:8787/multi` with form data
`animation.levels=0` again returns `animation.levels` or
`[0, 0, 0]` at the start.

2. `PUT`ting `http://localhost:8787/multi` with
form data `animation.levels=[1, 1, 1]&animation.master=0.5` sets the level of
all three animations to be `1`, and the `master` to be `0.5`.

3. `PUT`ting `http://localhost:8787/multi/master` with
form data `levels=[1, 1, 1]&master=0.5` does the same as the previous example.
