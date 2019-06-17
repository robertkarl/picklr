![demo.png]
# What's this?

Web app that emits Modern Horizons "pack one, pick one" ratings based on card titles.

Accepts shorthand card names, one per line. You can omit spaces or apostrophes.

This is useful for quickly rating cards in a pack during a draft, or for testing your knowledge of Frank Karsten's pick order.

Example:
```
alisman of creat
santusk
man-o-war
```

Yields the cards
```
Talisman of Creativity - 3.38

Man-o'-War - 3.35

Krosan Tusker - 3.16
```

This is not affiliated with Wizards of the Coast.

Card ratings from Frank Karsten's [Channel Fireball article](https://www.channelfireball.com/articles/a-very-early-pick-order-for-modern-horizons-draft/).

Ratings spreadsheet is on Google Sheets [here](https://docs.google.com/spreadsheets/d/e/2PACX-1vRiopQuQgB3fw_X4GNFIBJw5QMHmJJREGBFDZJwuYCwNGsU59rr_O1wc0u1RxV3xL602eHYQlax8HGv/pubhtml).


# The Combo
Deploying multiple flask apps with nginx and uwsgi

- Run the flask app with uwsgi. In your .ini use `mount = /desired_prefix=your_flask.app:app` or thereabouts.
- In your nginx config, use 
  ```
  location /picklr/ {
      include uwsgi_params;
      uwsgi_pass unix:/home/rk/code/picklr/picklr.sock;
  }
  ```
  or thereabouts.

